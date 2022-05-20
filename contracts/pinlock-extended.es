{
    // ===== Contract Information ===== //
    // Description: EgroScript contract for the grantor/beneficiary pinlock example.

    // ===== Hard-Coded Constants ===== //
    // val _GrantorPK: SigmaProp
    // val _BeneficiaryPK: SigmaProp

    // ===== Box Contents ===== //
    // value: Long     => ERGs sent by the grantor
    // registers:
    //  R4: Coll[Byte] => Blake2b256 hash bytes of the pin bytes

    // ===== Deposit Tx ===== //
    // Inputs: grantor box
    // Outputs: pinlock box

    // ===== Withdraw Tx ===== //
    // Inputs: pinlock box
    // Outputs: beneficiary box or grantor box, each with the correct pin value in R4

    (_GrantorPK || _BeneficiaryPK) && sigmaProp(SELF.R4[Coll[Byte]].get == blake2b256(OUTPUTS(0).R4[Coll[Byte]].get))
}