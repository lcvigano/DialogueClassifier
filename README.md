# 6.863 Final Project
## Analysis of Unique Syntactic Patterns in Television Dialogue for Character Classification
This project trains a neural network on dialogue said by Bart and Marge of the Simpsons TV show.

VM Note - Please use VMWare and allot 10 GB of memory and 2 CPUs to the VM.

## System Requirements (Already done on VM)
* Python 2.7
* Java 8
* Assumes running on Mac OS X or Ubuntu. Untested on Windows.

## Step 1 (Already done on VM)
Download the Stanford CoreNLP parser from this link.
https://stanfordnlp.github.io/CoreNLP/

Unpack/unzip the downloaded file and place in the project's top directory.


## Step 2
cd into the Stanford CoreNLP parser directory. Run this command to start the server.

`java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 150000`

The server will time out after 150,000 mS (150 seconds). If the server times out at some point, just re-run that command.

## Step 3
While the server is running, open a new terminal tab. cd into the data directory of this project. Run `python main.py`, passing in these arguments:
* `--test <test_data_file_path>`
* `--train <train_data_file_path>`
* `--person1 <person1_name>`
* `--person2 <person2_name>`

For example, you can type:

`python main.py --person1 'marge simpson' --person2 'bart simpson' --train_file training_data.txt --test_file testing_data.txt`


This will parse all of the sentence data using the Stanford CoreNLP parser, and create parse trees for each sentence and analyzes syntactic patterns of the speakers.

Note - if providing new test and train data from a different dataset, make sure it's in the correct format. The correct format can be seen in the `testing_data.txt` and `training_data.txt`. Make sure the names in the data files match the person1_name and person2_name passed in as arguments.

## Step 4
cd into the NET directory of this project. Run `python main.py`, passing in these arguments:
* `--train`
* `--test`
* `--model_file <model_file_path>`
* `--lr <lr_value>`
* `--wd <wr_value>`
* `--epochs <epochs_value>`
* `--batch_size <batch_size_value>`
* `--num_workers <num_workers_value>`

For example, to train with Marge and Bart data, run this command:

`python main.py --person1 'marge simpson' --person2 'bart simpson' --train`

To test the trained models, type:

`python main.py --person1 'marge simpson' --person2 'bart simpson' --test --model_file <model_file_name>.pt`

Models can be found in the models/ directory. Please move the desired model into the NET/ directory for testing.

