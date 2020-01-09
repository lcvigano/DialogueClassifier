import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data as data

class LSTM(nn.Module):

    def __init__(self, embeddings, args):
        super(LSTM, self).__init__()

        self.embeddings = embeddings
        vocab_size, embed_dim = embeddings.shape
        self.args = args

        self.lstm = nn.LSTM(input_size=300, hidden_size=args.hidden_dim,
                                batch_first=True, dropout=0.2, bidirectional=False)

        self.embedding_layer = nn.Embedding(vocab_size, embed_dim)
        self.embedding_layer.weight.data = torch.from_numpy(embeddings)

        self.W_out = nn.Linear(args.hidden_dim, 2)

        self.hidden = self.init_hidden()
        self.cell = self.init_cell()

    def init_hidden(self):
        return autograd.Variable(torch.zeros(16, 1, self.args.hidden_dim))

    def init_cell(self):
        return autograd.Variable(torch.zeros(16, 1, self.args.hidden_dim))


    def forward(self, x_indx):
        all_x = self.embedding_layer(x_indx)
        lstm_out, (self.hidden, self.cell) = self.lstm(all_x, (self.hidden.detach(), self.cell.detach()))
        clone = lstm_out.clone()
        lstm_out = lstm_out.mean(dim=1)
        return self.W_out(lstm_out)