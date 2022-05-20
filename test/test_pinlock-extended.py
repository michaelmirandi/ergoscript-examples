from hashlib import blake2b
import traceback
from ergo_python_appkit.appkit import ErgoAppKit, ErgoValueT
from org.ergoplatform.appkit import Address

# Test class
class TestPinlockExtended:
    
    # test variables
    appkit = ErgoAppKit("http://213.239.193.208:9053/", "mainnet", "https://api.ergoplatform.com/")
    grantorPK = Address.create("9fSek6bWQ2yusFHyJARD95KPTCrn5rfEav6msGZpxQZQvcBADQ9")
    beneficiaryPK = Address.create("9gcszEx4ev6YQQvxLDZhiWwuvxDnFDvdZkrAW9r9F7bhiHzj9gQ")
    pin = int(123)
    minerFee = int(1e6)

    # importing ErgoScript contract
    with open(f'contracts/pinlock-extended.es') as f:
        pinlockExtendedScript = f.read()

    # compile ErgoScript to ErgoTree
    pinlockExtendedTree = appkit.compileErgoScript(
        pinlockExtendedScript,
        {
            "_GrantorPK": grantorPK.getPublicKey(),
            "_BeneficiaryPK": beneficiaryPK.getPublicKey()
        }
    )

    # print the ErgoTree to see what it looks like
    print(f'Extended Pinlock ErgoTree: {pinlockExtendedTree.bytesHex()}')

    # deposit transaction
    def test_deposit(self):
        
        # input box
        grantorInputBox = self.appkit.buildInputBox(
            value = int(1000e9),
            tokens = None,
            registers = None,
            contract = self.appkit.contractFromAddress(self.grantorPK.toString()),
        )

        # output box of deposit transaction: pinlock box
        extendedPinlockOutputBox = self.appkit.buildOutBox(
            value = int(100e9),
            tokens = None,
            registers = [
                ErgoAppKit.ergoValue(blake2b(bytes(self.pin), digest_size=32).digest(), ErgoValueT.ByteArray)
            ],
            contract = self.appkit.contractFromTree(self.pinlockExtendedTree)
        )
        
        txCreated = False
        
        try: 
            # build the unsigned transaction
            depositUnsignedTx = self.appkit.buildUnsignedTransaction(
                inputs = [grantorInputBox],
                dataInputs = None,
                outputs = [extendedPinlockOutputBox],
                fee = self.minerFee,
                sendChangeTo = self.grantorPK.getErgoAddress()
            )
            txCreated = True
            
            # print unsigned tx
            print(ErgoAppKit.unsignedTxToJson(depositUnsignedTx))
        except:
            traceback.print_exc()
            txCreated = False
        
        assert txCreated
        
    # withdraw transaction    
    def test_withdraw(self):
        
        # input box of withdraw transaction: pinlock box
        extendedPinlockInputBox = self.appkit.buildInputBox(
            value = int(100e9),
            tokens = None,
            registers = [
                ErgoAppKit.ergoValue(blake2b(bytes(self.pin), digest_size=32).digest(), ErgoValueT.ByteArray)
            ],
            contract = self.appkit.contractFromTree(self.pinlockExtendedTree)
        )
        
        #output box of withdraw transaction: beneficiary box
        beneficiaryOutputBox = self.appkit.buildOutBox(
            value = int(100e9) - self.minerFee,
            tokens = None,
            registers = [
                ErgoAppKit.ergoValue(bytes(self.pin), ErgoValueT.ByteArray)
            ],
            contract = self.appkit.contractFromAddress(self.beneficiaryPK.toString()),
        )
        
        txCreated = False
        
        try: 
            # build the unsigned transaction
            withdrawUnsignedTx = self.appkit.buildUnsignedTransaction(
                inputs = [extendedPinlockInputBox],
                dataInputs = None,
                outputs = [beneficiaryOutputBox],
                fee = self.minerFee,
                sendChangeTo = self.beneficiaryPK.getErgoAddress()
            )
            txCreated = True
            
            # print unsigned tx
            print(ErgoAppKit.unsignedTxToJson(withdrawUnsignedTx))
        except:
            traceback.print_exc()
            txCreated = False
        
        assert txCreated
        