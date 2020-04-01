import pandas as pd
import numpy as np
import json
import datetime

def find_mode(narration):
    if "UPI" in narration:
        return "UPI"
    elif "ATM" in narration:
        return "ATM"
    elif "card" in narration:
        return "CARD"
    elif "TRANSFER" in narration:
        return "FT"
    else:
        return "OTHERS"


def deposit_generator(bank_statement_path):
    df = pd.read_csv(bank_statement_path, sep="\t",names=list(range(7)))[:-1]
    df.insert(0, 'row_num', range(0,len(df)))
    transactionRow = int(df.loc[df[0] == "Txn Date"]['row_num'].values[0])
    txnCols = df[df['row_num'] == transactionRow].drop(['row_num'], axis = 1) 
    transactionDetails = df[df['row_num']>transactionRow].drop(['row_num'], axis = 1)
    transactionDetails.columns = txnCols.values[0]
    txnDetails = transactionDetails.rename(columns={"Txn Date": "_transactionTimestamp", "Value Date": "_valueDate", 
                     "Description": "_narration", "Ref No./Cheque No.": "_reference", "Balance": "_currentBalance"})
    txnDetails.columns = txnDetails.columns.str.replace(' ', '')
    txnDetails = txnDetails.replace(r'^\s*$', np.nan, regex=True)
    txnDetails['_transactionTimestamp'] = txnDetails['_transactionTimestamp'].apply(lambda x: datetime.datetime.strptime(x, '%d %b %Y').strftime('%Y-%m-%d'))
    txnDetails['_valueDate'] = txnDetails['_valueDate'].apply(lambda x: datetime.datetime.strptime(x, '%d %b %Y').strftime('%Y-%m-%d'))

    txnDetails['_type'] = txnDetails.apply(lambda x: 'DEBIT' if np.isnan(float(str(x['Credit']).replace(",",""))) else 'CREDIT', axis=1)

    txnDetails['_amount'] = txnDetails.apply(lambda x: x['Credit'] if np.isnan(float(str(x['Debit']).replace(",",""))) else x['Debit'], axis=1)

    txnDetails = txnDetails.drop(['Credit', 'Debit'], axis = 1)

    txnDetails['_mode'] = txnDetails['_narration'].apply(find_mode)
    txnDetails['_txnId'] = np.arange(len(txnDetails))
    
    if "No" in df[df[0].str.contains("Nomination")][1].values[0]: 
        _nominee = "NOT-REGISTERED" 
    else: 
        _nominee = "REGISTERED"
        
    deposit = {
        "Account": {
            "Profile": {
                "Holders": {
                    "Holder": {
                        "_name": df[df[0].str.contains("Name")][1].values[0],
                        "_dob": "", #No reference
                        "_mobile": "", #No reference
                        "_nominee":  _nominee,
                        "_email": "", #No reference
                        "_pan": "", #No reference
                        "_ckycCompliance": "true" #No reference
                    },
                    "_type": "JOINT" #No reference
                }
            },
            "Summary": {
                "Pending": { #No reference
                    "_amount": "20.0" 
                },
                "_currentBalance": "0", #No reference
                "_currency": "INR", #No reference
                "_exchgeRate": "", #No reference
                "_balanceDateTime": datetime.datetime.strptime(df[df[0].str.contains("Date")][1].values[0], '%d %b %Y').strftime('%Y-%m-%d'),
                "_type": df[df[0].str.contains("Description")][1].values[0],
                "_branch": df[df[0].str.contains("Branch")][1].values[0],
                "_facility": "CC", #No reference
                "_ifscCode": df[df[0].str.contains("IFS")][1].values[0],
                "_micrCode": df[df[0].str.contains("MICR")][1].values[0],
                "_openingDate": "", #No reference
                "_currentODLimit": "", #No reference
                "_drawingLimit": df[df[0].str.contains("Drawing")][1].values[0],
                "_status": "ACTIVE" #No reference
            },
            "Transactions": {
                "Transaction": txnDetails.fillna("").to_dict(orient='records'),
            "_startDate": datetime.datetime.strptime(df[df[0].str.contains("Start Date")][1].values[0], '%d %b %Y').strftime('%Y-%m-%d'),
            "_endDate": datetime.datetime.strptime(df[df[0].str.contains("End Date")][1].values[0], '%d %b %Y').strftime('%Y-%m-%d'),
            },
            "_xmlns": "http://api.rebit.org.in/FISchema/deposit",
            "_xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "_xsi:schemaLocation": "http://api.rebit.org.in/FISchema/deposit ../FISchema/deposit.xsd",
            "_linkedAccRef": "",
            "_maskedAccNumber": df[df[0].str.contains("Number")][1].values[0],
            "_version": "1.1",
            "_type": "deposit"
        }
    }
    
    return json.dumps(deposit)
