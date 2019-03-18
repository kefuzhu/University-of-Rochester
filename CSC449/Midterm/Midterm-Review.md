# CSC 449 Midterm Review

## 1. Linear Filtering

Linear filtering is filtering in which the value of an output pixel is a linear combination of the values of the pixels in the input pixel's neighborhood

## 2. Correlation vs. Convolution

- Filter kernel $H$ has size of $(2k+1) \times (2k+1)$
- Image $F$

	**(1) Correlation (Cross-Correlation)**: $G = H \otimes F$
	
	<center>
	$G[i,j] = \sum_{u = -k}^k \sum_{v = -k}^k H[u,v]F[i+u,j+v]$
	</center>

	**(2) Convolution**: $G = H * F$
	
	<center>
	$G[i,j] = \sum_{u = -k}^k \sum_{v = -k}^k H[u,v]F[i-u,j-v]$
	</center>
	
**Note**: Performing convolution is the same as performing correlation using the flipped filter kernel

## 3. Gaussian Filter

<center>
$H(u,v) = \frac{1}{2\pi\sigma^2}\exp(-\frac{u^2+v^2}{2\sigma^2})$
![](graphs/gaussian-filter.png)
</center>

- Remove high-frequency components from the image (low-pass filter)
- Convolution with self is another Gaussian
	- So can smooth with small $\sigma$ kernel, repeat, and get same result as larger $\sigma$ kernel would have
	- Convolving two times with Gaussian kernel with $\sigma$ is same as convolving once with kernel with $\sigma\sqrt{2}$ 
- Separable kernel
<center>
$H(u,v) = \frac{1}{2\pi\sigma^2}\exp(-\frac{u^2+v^2}{2\sigma^2}) = [\frac{1}{\sigma\sqrt{2\pi}}\exp(-\frac{u^2}{2\sigma^2})][\frac{1}{\sigma\sqrt{2\pi}}\exp(-\frac{v^2}{2\sigma^2})]$
</center>

	**Discrete Example**:
	<center>
	$
	\begin{bmatrix}
	1 & 2 & 1 \\
	2 & 4 & 2 \\
	1 & 2 & 1 \\
	\end{bmatrix} = 
	\begin{bmatrix}
	1 \\
	2 \\
	1 \\
	\end{bmatrix}
	\begin{bmatrix}
	1 & 2 & 1 
	\end{bmatrix}
	$
	</center>

## 4. Edge

**(1) What is an edge?** An edge is a place of rapid change in the image intensity function

**(2) What causes an edge?**

<center>
![](graphs/edge-1.png)
</center>

- Refelectance change: appearance information, texture
- Depth discontinuity: object boundary
- Change in surface orientation: shape
- Cast shadows

**(3) How to extract edges from image?**

We can extract edges by computing the gradient of an image, 

<center>
$\nabla f = [\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}]$
</center>

Computing the derivative is the same as convolving the image with specific filters

<center>
![](graphs/edge-convolve.png)
</center>

where the gradient points in the direction of most rapid increase in intensity, which is perpendicular to the direction of the edge.

<center>
![](graphs/image-gradient.png)
</center>

- The gradient direction is given by: $\theta = \tan^{-1}(\frac{\partial f}{\partial y}/\frac{\partial f}{\partial x})$
- The edge strength is given by the gradient magnitude: $||\nabla f|| = \sqrt{(\frac{\partial f}{\partial x})^2+(\frac{\partial f}{\partial y})^2}$

**(4) Gaussian Smoothing and Derivative Filter**

If the image has noises, it is hard to detect the real edge by only computing the gradient of the image. 

<center>
![](graphs/edge-noise.png)
</center>

Therefore, we usually will perform smoothing on the image first and then take the gradient. The peak (maxima) of the $\frac{\partial}{\partial x}(h * f)$ corresponds to the edge. 

<center>
![](graphs/edge-smooth.png)
</center>

**Derivative theorem of convolution**

Because differentiation is convolution, and convolution is associative. We have:

By convolving the image with the derivative of filter directly, we save one step and improve efficency

<center>
$\frac{\partial}{\partial x}(h * f) = (\frac{\partial}{\partial x}h) * f$
</center>

<center>
![](graphs/edge-derivative.png)
</center>

In 2-D image, the derivative of gaussian filter is different (rotate 90 degree) for $\mathrm{x}$ and $\mathrm{y}$ direction

<center>
![](graphs/edge-gaussian-derivative.png)
</center>

Rather than finding the maxima in the first derivative gaussian operator, we consider finding the zero-crossing of the convolving result between second derivative of gaussian operator (**Laplacian of Gaussian operator $\nabla^2$**) and the image

<center>
$\nabla^2f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} $
![](graphs/edge-gaussian.png)
![](graphs/edge-laplacian.png)
</center>


**Effect of Scale**: Tradeoff between detection and localization

**a. Detection**: responds to edges; does not respond to noise

**b. Localization**: maximum of convolution result is as near as possible to the true edge location

- Don't smooth (No Gaussian filter/Gaussian filter with small scale $\sigma$) 

	$\rightarrow$ **Lose accuracy of detection**: Detect too many edges (some are noises) 
- Smooth too much (Gaussian filter with large sacle $\sigma$)

	$\rightarrow$ **Lose localization**: Detect edges are fatter than they suppose to be / lose edges very close to each other 
	
<center>
![](graphs/edge-scale.png)
</center>

**Review: Smoothing vs. derivative filters**

- **Smoothing filters**
	- Gaussian: remove "high-frequency" components; "low-pass" filter
	- The values of a smoothing filter cannot be negative
	- The values of a smoothing filter sum to
		- **One**: Constant regions are not affected by the filter 
- **Derivative fitlers**
	- Derivatives of Gaussian 
	- The values of a derivative filter can be negative
	- The values of a derivative filter sum to
		- **Zero**: No response in constant regions
	- High absolute value at points of high contrast 

## 5. Corner

**(1) What is a corner (interest point) in image?**