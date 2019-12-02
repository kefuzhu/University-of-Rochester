#!/usr/bin/env Rscript

# Load library
suppressWarnings(suppressMessages(library(sf)))
suppressWarnings(suppressMessages(library(lubridate)))
suppressWarnings(suppressMessages(library(progress)))
suppressWarnings(suppressMessages(library(optparse)))

####################
# Helper Functions #
####################

# Point-in-Polygon Detection
coordinate_in_polygon = function(lat, long, polygon){
  # Input:
  # - lat: GPS latitude
  # - long: GPS longitude
  # - polygon: sfc_MULTIPOLYGON (usually from a shapefile)
  
  # Output:
  # - TRUE/FALSE: Whether the input point is within the multi-polygons
  
  # Create simple feature in sf
  sf_point = st_point(c(long,lat))
  # Convert simple feature to simple feaature geometry list 
  # Note: Since input is GPS coordinate, crs = 4326 is used (https://spatialreference.org/ref/epsg/wgs-84/)
  sf_point = st_sfc(sf_point, crs = 4326)
  # Transform to palnar (crs = 2163) because sf library assumes planar projection
  sf_point = st_transform(sf_point, crs = 2163)
  
  # Transform the multipolygon to palnar 
  geofence = st_transform(polygon, crs = 2163)
  # sparse = FALSE returns a logical matrix
  # with rows corresponds to argument 1 (points) and 
  # columns to argument 2 (polygons)
  return(as.vector(st_intersects(sf_point, geofence, sparse = FALSE)))
}

# MultiplePoints-in-Polygon Detection
MultipleCoordinate_in_polygon = function(coordinate, polygon){
  # Input:
  # - coordinate: dataframe object where the first column is longtitude and second column is latitude
  # - polygon: sfc_MULTIPOLYGON (usually from a shapefile)
  
  # Output:
  # - TRUE/FALSE: Whether each point is within the multi-polygons
  
  # Create a collection of GPS coordinates
  sf_points = do.call("st_sfc",
                      c(lapply(1:nrow(coordinate), 
                               function(i) {st_point(as.numeric(coordinate[i, ]))}), 
                        list("crs" = 4326)))
  # Transform to palnar (crs = 2163) because sf library assumes planar projection
  sf_points <- st_transform(sf_points, 2163)
  # Transform the multipolygon to palnar
  geofence = st_transform(polygon, crs = 2163)
  # sparse = FALSE returns a logical matrix
  # with rows corresponds to argument 1 (points) and 
  # columns to argument 2 (polygons)
  return(st_intersects(sf_points, geofence, sparse = FALSE))
}

# Preprocess the warning data from NWS
warning_preprocess = function(path, phenom_list, verbose = FALSE){
  # Input: 
  # - path: input file path
  # - phenom_list: list of phenomenon used for data filtering
  
  # Output:
  # - warning_data: preprocessed warning data as DataFrame object
  
  # Required library
  require(sf)
  
  # Read in the data
  # Read the NWS warning data
  warning_data = st_read(path)
  if(verbose){
    writeLines('Read the NWS warning data...')
    writeLines('')
  }
  
  # Convert the shape file data into DataFrame object
  if(verbose){
    writeLines('Converting shape file data into DataFrame object...')
  }
  warning_data = data.frame(warning_data)
  # Only keep storm related records
  if(verbose){
    writeLines('Only keep storm related records...')
  }
  warning_data = warning_data[sapply(warning_data$PHENOM, function(x) x %in% phenom_list),]
  # Only keep the warning records
  if(verbose){
    writeLines('Only keep warning records...')
  }
  warning_data = warning_data[warning_data$SIG == 'W',]
  # Convert time columns to numeric values
  if(verbose){
    writeLines('Converting time related columns from factor to numeric values...')
  }
  warning_data$ISSUED = as.numeric(as.character(warning_data$ISSUED))
  warning_data$EXPIRED = as.numeric(as.character(warning_data$EXPIRED))
  warning_data$INIT_ISS = as.numeric(as.character(warning_data$INIT_ISS))
  warning_data$INIT_EXP = as.numeric(as.character(warning_data$INIT_EXP))
  # Create two new columns: start, end
  if(verbose){
    writeLines("Compute MIN and MAX timestamp and store in two new columns, 'start' and 'end'...")
  }
  warning_data['start'] = apply(data.frame(warning_data$ISSUED, 
                                           warning_data$EXPIRED, 
                                           warning_data$INIT_ISS, 
                                           warning_data$INIT_EXP), 1, min)
  warning_data['end'] = apply(data.frame(warning_data$ISSUED, 
                                         warning_data$EXPIRED, 
                                         warning_data$INIT_ISS, 
                                         warning_data$INIT_EXP), 1, max)
  
  if(verbose){
    writeLines('')
    writeLines('Warning data preprocessing is complete!')
    writeLines('--------------------------------------------------------')
  }
  
  # Output
  return(warning_data)
}

# Convert datetime object to numeric value for comparison purpose
datetime_to_numeric = function(datetime){
  # Input: datetime, "POSIXlt" or "POSIXt" time object
  # Output: Numeric value representation of input time object
  
  # Note: The numeric value is designed to align with the time provided in NWS warning data
  
  # Required library
  require(lubridate)
  
  numeric_value = (year(datetime) * 10^8) +
                  (month(datetime) * 10^6) +
                  (day(datetime) * 10^4)
  
  return(numeric_value)
}

# Main function to match warning records with a list of POI
match_warning = function(warning_data, POI, mergeSize, startDate, endDate, specific_event = FALSE, event_date, window_size, show_progress = FALSE, verbose = FALSE){
  # Input:
  # - warning_data: preprocessed warning data as DataFrame object
  # - POI: DataFrame object contains POI in each row. First column is longitude, second column is latitude
  # - mergeSize: the number of days used as creterion to merge 
  #              different warnings for the samae event together
  #   The search window can either between:
  #   - startDate: start date of search window in the format of YYYYMMDD
  #   - endDate: end date of search window in the format of YYYYMMDD
  #   or focus on a specific storm with certain window size
  #   - specific_event: TRUE/FALSE
  #   - event_date: the date of storm event in the format of YYYYMMDD
  #   - window_size: look for time interval from `window_size` days ahead to 
  #                  `window_sizee` days after
  # - show_progress: Show the progress of matching operation
  

  # Required library
  require(progress)
  
  if(verbose){
    writeLines('Subset the warning data based on search window...')
    writeLines('')
  }
  
  # Match data type
  startDate = strptime(startDate, '%Y%m%d')
  endDate = strptime(endDate, '%Y%m%d')
  # Convert time to numeric value
  startDate = datetime_to_numeric(startDate)
  endDate = datetime_to_numeric(endDate)
  
  # Warnings that are within the search window
  match_time = (warning_data$start > startDate) & (warning_data$end < endDate)
  # Subset warnings based on above conditions
  warning_data = warning_data[match_time,]
  
  if(verbose){
    writeLines('Match warning records within the search window...')
    writeLines('')
  }

  # Boolean vector to indicate which warning affects the POI
  bool_vec = c()
  # Progress bar
  if(show_progress == TRUE){
      pb <- progress_bar$new(
        format = "  Progress :spin [:bar] :elapsedfull :percent ETA: :eta",
        total = nrow(warning_data)+1, clear = FALSE, width = 60)
  }

  # Iterate over every warning
  for(i in 1:nrow(warning_data)){
    
    # Geofence of the current warning
    geofence = warning_data$geometry[i]
    # TRUE/FALSE: Whether the each POI is impacted by the warning region
    within_geofence = MultipleCoordinate_in_polygon(coordinate = POI, polygon = geofence)
    # If the any POI is affected by the weather
    if(any(within_geofence)){
      bool_vec[i] = TRUE
    } else{
      bool_vec[i] = FALSE
    }

    # Progress bar increment
    if(show_progress == TRUE){
      pb$tick()
    }
  }

  # Warnings
  warnings = warning_data[bool_vec, c('PHENOM','start','end')]
  
  if(verbose){
    writeLines('Sort the warning records by start date in chronological order...')
    writeLines('')
  }
  
  # Sort warning data by start date in chronological order
  warnings = warnings[order(warnings$start, decreasing = FALSE),]

  # Reset row names
  rownames(warnings) = NULL

  if(verbose){
    writeLines('Matching Operation Completed!')
    writeLines('')
  }
  return(warnings)  
}

#################
# Main Function #
#################

main = function(warning_data, phenom, 
                specific_event = FALSE, event_date, window_size, 
                startDate, endDate, merge = FALSE,
                merge_threshold, show_progress = FALSE){

  ###################################
  # Step 1. Point of Interest (POI) #
  ###################################
 
  Manhattan_POI = c(-73.911311,40.822447)
  Staten_Island_POI = c(-74.151583,40.584470)
  Brooklyn_POI_1 = c(-73.890981,40.724087)
  Brooklyn_POI_2 = c(-73.952338,40.637431)
  Queens_POI = c(-73.768385,40.719720)
  Rockaway_POI = c(-73.820166,40.585415)
  POI_df = rbind(Manhattan_POI, Staten_Island_POI, Brooklyn_POI_1, Brooklyn_POI_2, Queens_POI, Rockaway_POI)

  #################################
  # Step 2. Load NWS Warning Data #
  #################################
  
  # Load and preprocess the warning data from NWS
  NWS_warning = warning_preprocess(path = warning_data, phenom_list = phenom, verbose = TRUE)
  
  #########################################################
  # Step 3. Extract Warning Records winthin search window #
  #########################################################
  
  writeLines('Extract warning records within search window')

  warning_subset = match_warning(warning_data = NWS_warning, 
                                 POI = POI_df,
                                 startDate = startDate, endDate = endDate, 
                                 verbose = TRUE, show_progress = show_progress)
  
  writeLines('')
  
  return(warning_subset)
}

##################################
# Code that is actually executed #
##################################

# NWS Warning data
warning_data = '../data/NWS-warnings/2018_all/wwa_201801010000_201812312359.shp'
# Start date
start_date = '20180101'
# End date
end_date = '20181231'
# Weather list
weather_list = 'HF,HU,IS,SQ,SR,SS,SV,WS,BZ,LE,WC,EC,TO'
weather_list = unlist(strsplit(weather_list, split=','))
# Output location
output = '../data/NYC_2018_weather.csv'


match_result = main(warning_data = warning_data, phenom = weather_list, startDate = start_date, endDate = end_date, show_progress = TRUE)

# Write result to output location
writeLines(paste(c('Writing result to output location: ',output,' ...'), collapse = ''))
write.csv(match_result, file = output, row.names = FALSE)
writeLines('')
writeLines('Completed!')

# Garbarge collect
gc()
