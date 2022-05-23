from hashlib import blake2b
import traceback
from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import Address

class TestSimpleSend:

    appkit = ErgoAppKit("http://213.239.193.208:9053/", "mainnet", "https://api.ergoplatform.com/")
    alicePk = Address.create("9fSek6bWQ2yusFHyJARD95KPTCrn5rfEav6msGZpxQZQvcBADQ9")
    bobPk = Address.create("9gcszEx4ev6YQQvxLDZhiWwuvxDnFDvdZkrAW9r9F7bhiHzj9gQ")
    deadline = int(756872 + 15)
    minerFee = int(1e6)

    # importing ErgoScript contract
    with open(f'contracts/simple-send.es') as f:
        timeFundedScript = f.read()

    # compile ErgoScript to ErgoTree
    timeFundedTree = appkit.compileErgoScript(timeFundedScript, {
        '_alicePk': alicePk.getPublicKey(),
        '_bobPk': bobPk.getPublicKey(),
        '_deadline': deadline
    })

    print(f'Extended Time Funded ErgoTree: {timeFundedTree.bytesHex()}')

    def test_alice_deposit(self):
        aliceInputBox = self.appkit.buildInputBox(
            value = int(1000e9),
            tokens = None,
            registers = None,
            contract = self.appkit.contractFromAddress(self.alicePk.toString()),
        )

        timelockOutputBox = self.appkit.buildOutBox(
            value= int(10e9),
            tokens=None,
            registers=None,
            contract = self.appkit.contractFromTree(self.timeFundedTree)
        )

        txCreated = False

        print(timelockOutputBox.getCreationHeight())

        try:
            # build the unsigned transaction
            depositUnsignedTx = self.appkit.buildUnsignedTransaction(
                inputs = [aliceInputBox],
                dataInputs = None,
                outputs = [timelockOutputBox],
                fee = self.minerFee,
                sendChangeTo = self.alicePk.getErgoAddress()
            )
            txCreated = True
            
            # print unsigned tx
            print(ErgoAppKit.unsignedTxToJson(depositUnsignedTx))
            print('Should succeed', self.appkit.signTransaction(depositUnsignedTx))
        except: 
            traceback.print_exc()
            txCreated = False

        assert txCreated

    def test_alice_withdraw(self): 

        timelockInputBox = self.appkit.buildInputBox(
            value= int(10e9),
            tokens=None,
            registers=None,
            contract = self.appkit.contractFromTree(self.timeFundedTree)
        )

        aliceOutputBox = self.appkit.buildOutBox(
            # minus a transaction fee (platform)
            value = int(10e9) - self.minerFee,
            tokens = None,
            registers = None,
            contract = self.appkit.contractFromAddress(self.alicePk.toString()),
        )

        txCreated = False

        try:
            # build the unsigned transaction
            withdrawUnsignedTx = self.appkit.buildUnsignedTransaction(
                inputs = [timelockInputBox],
                dataInputs = None,
                outputs = [aliceOutputBox],
                fee = self.minerFee,
                sendChangeTo = self.alicePk.getErgoAddress()
            )
            txCreated = True
            
            # print unsigned tx
            print('Should fail', ErgoAppKit.unsignedTxToJson(withdrawUnsignedTx))
            print('Should fail', ErgoAppKit.signTransaction(unsignedTx=withdrawUnsignedTx))

        except: 
            traceback.print_exc()
            txCreated = False

        assert txCreated
        
    def test_bob_withdraw(self): 

        timelockInputBox = self.appkit.buildInputBox(
            value= int(10e9),
            tokens=None,
            registers=None,
            contract = self.appkit.contractFromTree(self.timeFundedTree)
        )

        bobOutputBox = self.appkit.buildOutBox(
            # minus a transaction fee (platform)
            value = int(10e9) - self.minerFee,
            tokens = None,
            registers = None,
            contract = self.appkit.contractFromAddress(self.bobPk.toString()),
        )

        txCreated = False

        try:
            # build the unsigned transaction
            withdrawUnsignedTx = self.appkit.buildUnsignedTransaction(
                inputs = [timelockInputBox],
                dataInputs = None,
                outputs = [bobOutputBox],
                fee = self.minerFee,
                sendChangeTo = self.bobPk.getErgoAddress()
            )
            txCreated = True
            
            # print unsigned tx
            print(ErgoAppKit.unsignedTxToJson(withdrawUnsignedTx))
        except: 
            traceback.print_exc()
            txCreated = False

        assert txCreated
        
