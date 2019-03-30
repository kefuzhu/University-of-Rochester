import torch
import torch.nn as nn
import torchvision.models as models
from torch.nn.utils.rnn import pack_padded_sequence
import torch.autograd as autograd
from torch.autograd import Variable
import math

class LSTMCell(nn.Module):
    """
    LSTM cell implementation
    Given an input x at time step t, and hidden and cell states: hidden = (h_(t-1), c_(t-1)),
    you will implement a LSTM unit to compute and return (h_t, c_t)
    hints: consider use linear layers to implement the several matrices W_* 
    Note: you just need to implement a one-layer LSTM unit
    """
    def __init__(self, input_size, hidden_size):
        super(LSTMCell, self).__init__()
        # TODO:
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.gate = nn.Linear(input_size + hidden_size, hidden_size)
        self.sigmoid = nn.Sigmoid()
        self.output = nn.Linear(hidden_size,input_size)
        self.tanh = nn.Tanh()
     

    def forward(self, x, hidden):
        # TODO:

        # Extract h and C from previous stage
        ht_prev, Ct_prev = hidden 
        # Stack ht_prev and x together
        stack = torch.cat((x, ht_prev), 1)

        # Compute the gates
        f_gate = self.gate(stack)
        i_gate = self.gate(stack)
        o_gate = self.gate(stack)
        # Add sigmoid function on top
        f_gate = self.sigmoid(f_gate)
        i_gate = self.sigmoid(i_gate)
        o_gate = self.sigmoid(o_gate)
        #
        Ct_tilde = self.gate(stack)
        Ct_tilde = self.tanh(Ct_tilde)
        Ct = torch.add(torch.mul(ht_prev,f_gate),torch.mul(Ct_tilde, i_gate))
        ht = torch.mul(self.tanh(Ct), o_gate)

        hidden = (ht, Ct)
        return hidden

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LSTM, self).__init__()

        self.hidden_size = hidden_size # dimension of hidden states
        self.lstmcell = LSTMCell(input_size, hidden_size)

    def forward(self, x, states):
        h0, c0 = states
        outs = []
        cn = c0[0, :, :]
        hn = h0[0, :, :]
        for seq in range(x.size(1)):
            hn, cn = self.lstmcell(x[:, seq, :], (hn, cn))
            outs.append(hn)
        out = torch.stack(outs, 1)
        states = (hn.unsqueeze(0), cn.unsqueeze(0))
        return out, states

class Encoder(nn.Module):
    def __init__(self, embed_size):
        """Load the pretrained ResNet-152 and replace top fc layer."""
        super(Encoder, self).__init__()
        resnet = models.resnet152(pretrained=True)
        modules = list(resnet.children())[:-1]      # delete the last fc layer.
        self.resnet = nn.Sequential(*modules)
        self.linear = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)
        
    def forward(self, images):
        """Extract feature vectors from input images."""
        with torch.no_grad():
            features = self.resnet(images)
        features = features.reshape(features.size(0), -1)
        features = self.bn(self.linear(features))
        return features


class Decoder(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers, max_seq_length=20):
        """Build the layers in the decoder."""
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.embed = nn.Embedding(vocab_size, embed_size) # word embedding
        
        # TODO: when you use your implemented LSTM, please comment the following
        # line and uncomment the self.lstm = LSTM(embed_size, hidden_size)
        # self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True) 
        self.lstm = LSTM(embed_size, hidden_size)
        
        self.linear = nn.Linear(hidden_size, vocab_size) # project the outputs from LSTM to vocabulary space
        self.max_seg_length = max_seq_length # max length of sentence used during inference
        
    def forward(self, features, captions, lengths):
        """Decode image feature vectors and generates captions."""
        
        # initialize the hidden state and cell state
        states = (autograd.Variable(torch.zeros(1, features.size(0), self.hidden_size).cuda()),
                  autograd.Variable(torch.zeros(1, features.size(0), self.hidden_size).cuda()))
        
        # TODO: you are required to build the decoder network based on the defined layers
        # in the init function. As discussed in the class, there are four steps: 
        # (1) extract word embeddings from captions; 
        # (2) concatenate visual feature (features, bx1xd) and extracted word embedding (bxtxd) and obtain the new features (bx(t+1)xd); 
        # (3) feed the new features into LSTM with the initialized states; 
        # (4) use a linear layer to project the feature to vocabulary space for training with a cross-entropy loss function. 

        # (1) Extract word embedding from caption
        embeddings = self.embed(captions)
        # (2) Concatenate visual feature and word embedding
        embeddings = torch.cat((features.unsqueeze(1), embeddings), 1)
        # (3) Feed forward in LSTM
        hiddens, _ = self.lstm(embeddings, states)
        # (4) Project feature
        outputs = self.linear(hiddens) # outputs: (batch_size, t+1, vocab_size)
        # do not change the following code
        outputs =  pack_padded_sequence(outputs, lengths, batch_first=True)
        return outputs[0]
    
    def sample(self, features, states=None):
        """Generate captions for given image features with a word-by-word scheme."""
        
        sampled_ids = []
        inputs = features.unsqueeze(1)
        states = (autograd.Variable(torch.zeros(1, inputs.size(0), self.hidden_size).cuda()),
                  autograd.Variable(torch.zeros(1, inputs.size(0), self.hidden_size).cuda()))
 
        for i in range(self.max_seg_length):
            hiddens, states = self.lstm(inputs, states)          # hiddens: (batch_size, 1, hidden_size)
            outputs = self.linear(hiddens.squeeze(1))            # outputs:  (batch_size, vocab_size)
            _, predicted = outputs.max(1)                        # predicted: (batch_size)
            sampled_ids.append(predicted)
            inputs = self.embed(predicted)                       # inputs: (batch_size, embed_size)
            inputs = inputs.unsqueeze(1)                         # inputs: (batch_size, 1, embed_size)
        sampled_ids = torch.stack(sampled_ids, 1)                # sampled_ids: (batch_size, max_seq_length)
        return sampled_ids
