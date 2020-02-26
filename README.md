# deposit_generator_aa
Generated AA compliant deposit - JSON by taking CSV of the bank statement from SBI
https://specifications.rebit.org.in/api_schema/account_aggregator/documentation/deposit.html

Download the XLS format of bank statement from SBI Internet Banking, convert XLS to CSV

#### Clone repo and check for conda -
```
git clone https://github.com/abraj09/deposit_generator_aa.git
cd deposit_generator_aa
conda --version
```
#### If error, then install conda using the following steps -

- for MacOS
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
sh Miniconda3-latest-MacOSX-x86_64.sh
```
- for Linux
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

#### After conda installation is complete, restart terminal-
```
conda create -n temp_env_gen python=3.7
conda activate temp_env_gen
pip install -r requirements.txt
python
```
#### Within python shell
```
from generator import deposit_generator
bank_statement_path = "path/to/csv/bank/statement"
deposit_generator(bank_statement_path)
```

PS. This is currently supported for SBI bank statement only
