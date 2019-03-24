import torch
import torchvision
import torchvision.transforms as transforms

import torch.nn as nn

import torch.optim as optim



classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# by default, we ship the data to GPU 0. you can sepcify it later
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

def build_data_loader(batch_size=4, num_workers=2, is_shuffle=True):
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                              shuffle=is_shuffle, num_workers=num_workers)

    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                             shuffle=False, num_workers=num_workers)
    return trainloader, testloader

class Net(nn.Module):
    """CNN model. Do not modify this class, but you are welcome to see the intermedia result of it"""
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(32, 32, 3, padding=1)
        self.relu2 = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(32, 6, 5)
        self.relu3 = nn.ReLU(inplace=True)
        self.conv4 = nn.Conv2d(6, 16, 5)
        self.relu4 = nn.ReLU(inplace=True)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.relu5 = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(120, 84)
        self.relu6 = nn.ReLU(inplace=True)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.pool1(self.relu2(self.conv2(x)))
        x = self.relu3(self.conv3(x))
        x = self.pool2(self.relu4(self.conv4(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = self.relu5(self.fc1(x))
        x = self.relu6(self.fc2(x))
        x = self.fc3(x)
        return x


def train(trainloader, net, optimizer, criterion, epoch=6):
    # TODO: implement the training code here

    running_loss = 0.0
    # Iteration
    for iteration in range(epoch):
        # Mini batch
        for i,data in enumerate(trainloader, 0):
            # Extract inputs and labels
            inputs, labels = data
            # Send to GPU if needed
            inputs, labels = inputs.to(device), labels.to(device)
            # Set gradient to zero
            optimizer.zero_grad()

            # Feed Forward
            outputs = net(inputs)
            # Compute loss
            loss = criterion(outputs,labels)
            # Backpropagation
            loss.backward()
            # Adjust the weight matrix with based on gradients
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (iteration + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')


def test(testloader, net):
    # test over whole dataset
    correct = 0
    total = 0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            c = (predicted == labels).squeeze()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    print('Accuracy of the network on the 10000 test images: %d %%' % (
        100 * correct / total))
    for i in range(10):
        print('Accuracy of %5s : %2d %%' % (
            classes[i], 100 * class_correct[i] / class_total[i]))


if __name__ == '__main__':
    # build dataloader
    train_loader, test_loader = build_data_loader(batch_size=4, num_workers=2, is_shuffle=True)

    # initialize model
    net = Net()
    net.to(device)

    # use crossentropy loss
    criterion = nn.CrossEntropyLoss()
    # use sgd optimizer
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    # train
    train(train_loader, net, optimizer, criterion, epoch=6)

    # save model, do not modify it.
    savepath = 'classifier_param.pth'
    torch.save(net.state_dict(), savepath)

    # test
    test(test_loader, net)

