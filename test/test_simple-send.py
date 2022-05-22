from hashlib import blake2b
import traceback
from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import Address

class TestSimpleSend:

    appkit = ErgoAppKit("http://213.239.193.208:9053/", "mainnet", "https://api.ergoplatform.com/")
    senderPk = Address.create("9fSek6bWQ2yusFHyJARD95KPTCrn5rfEav6msGZpxQZQvcBADQ9")
    recieverPk = Address.create("9gcszEx4ev6YQQvxLDZhiWwuvxDnFDvdZkrAW9r9F7bhiHzj9gQ")
    minerFee = int(1e6)

# importing ErgoScript contract
    with open(f'contracts/simple-send.es') as f:
        simpleSendScript = f.read()

    # compile ErgoScript to ErgoTree
    simpleSendTree = appkit.compileErgoScript(simpleSendScript)
    def test_deposit(self):
        

        senderInputBox = self.appkit.buildInputBox(
            value = int(1000e9),
            tokens = None,
            registers = None,
            contract = self.appkit.contractFromAddress(self.senderPk.toString()),
        )

        trueBox = self.appkit.buildOutBox(
            value = int(10e9),
                tokens = None,
                registers = None,
                contract = self.appkit.contractFromTree(self.simpleSendTree),
            )

        txCreated = False


        try:
            depositUnsignedTx = self.appkit.buildUnsignedTransaction(
                        inputs = [senderInputBox],
                        dataInputs = None,
                        outputs = [trueBox],
                        fee = self.minerFee,
                        sendChangeTo = self.senderPk.getErgoAddress()
                    )

            txCreated = True
            print(ErgoAppKit.unsignedTxToJson(depositUnsignedTx))
        except:
            traceback.print_exc()
            txCreated = False

        assert txCreated
    