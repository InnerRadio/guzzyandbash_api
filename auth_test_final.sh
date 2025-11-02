#!/bin/bash
set+#hisdisableshistoryexpansiontopreventisseswith'!'

#---nvironmentariables(tomaticallysetforyorconvenience)---
_"https//gzzyandbash.com"
_"gzzy_sperser"
_'estassword!'#!
_"admingzzyandbash.com"

#---perser(forcreator_ser_idinmintingandotherspecificcalls)---
_"b-ef--d-cbbbca"#djstifyorsperserhasadifferent

#---ariablesfordynamicdata(poplatedatomaticallydringscriptexection)---
_""
_""
#hesewillbepoplateddringthisscriptexection

echo"---llenvironmentvariablesarenowdefinedwithinthisscript.---"
echo"---nsring'jq'isinstalledfordynamicparsing...---"
if!command-vjq&/dev/nll
then
echo"'jq'isnotinstalled.leaseinstall'jq'(e.g.,'sdoapt-getinstalljq'or'brewinstalljq')forthisscripttorncorrectly."
exit
fi
echo"---'jq'fond.roceeding.---"


#---.thenticationndpoints---

echo-e"n---ectionthenticationndpoints---"

#../api/v/ath/login-oginorccessoken(tomatedaptre)
#rposeynamicallygetandsetthelatesttokensforsbseqentreqests.
echo-e"n---esting$_/api/v/ath/login---"
_$(crl-s-
"$_/api/v/ath/login"
-"acceptapplication/json"
-"ontent-ypeapplication/x-www-form-rlencoded"
-d"grant_typepassword&sername$_&password$_")

_$(echo"$_"|jq-r'.access_token')
_$(echo"$_"|jq-r'.refresh_token')

echo"oginesponse$_"
echo"aptred_$_"
echo"aptred_$_"


#../api/v/ath/register-egisterser(orrected&ashscape)
#rposereateanewseraccont.
echo-e"n---esting$_/api/v/ath/register---"
_"test_new_ser_$(date+%s%|ct-b-)"
_"test_new_ser_$(date+%s%|ct-b-)example.com"

#oteegistrationwith'role'and'is_verified'sallyreqiresadmin/sperserprivileges.
#hiscrlcommandincldesthethorizationheadersingtheperser'stoken.
crl-"$_/api/v/ath/register"
-"acceptapplication/json"
-"ontent-ypeapplication/json"
-"thorizationearer$_"
-d"{
"sername""$_",
"email""$_",
"password""estassword!",
"fll_name""ewegisteredestser",
"role""registered_ser",
"ser_types"],
"is_verified"false
}"

#../api/v/ath/token/refresh-efreshccessoken(orrectedpayloadandheader)
#rposeetanewaccesstokensingyorrefreshtoken.
echo-e"n---esting$_/api/v/ath/token/refresh---"
crl-v-
"$_/api/v/ath/token/refresh"
-"acceptapplication/json"
-"ontent-ypeapplication/x-www-form-rlencoded"
-"thorizationearer$_"
-d"grant_typerefresh_token&refresh_token$_"

#../api/v/ath/password-reset-reqest-eqestasswordeset
#rposenitiateapasswordresetprocessforanemail.
echo-e"n---esting$_/api/v/ath/password-reset-reqest---"
#singaplaceholderemailreplacewitharealseremailifyowanttotestemailsending.
crl-
"$_/api/v/ath/password-reset-reqest"
-"acceptapplication/json"
-"ontent-ypeapplication/json"
-d'{
"email""any_registered_serexample.com"}'

#../api/v/ath/password-reset-confirm-onfirmasswordeset(orrectedieldame)
#rposeonfirmpasswordresetwithatoken(e.g.,fromemail)andnewpassword.
echo-e"n---esting$_/api/v/ath/password-reset-confirm---"
#oteomanallyreplace"___"withanactaltokeniftesting.
crl-
"$_/api/v/ath/password-reset-confirm"
-"acceptapplication/json"
-"ontent-ypeapplication/json"
-d'{
"token""___",
"new_password""ewtrongassword!",
"new_password_confirm""ewtrongassword!"
}'

#avetokensandperserforsbseqentsections
echo"$_"./.ath_token.tmp
echo"$_"./.refresh_token.tmp
echo"$_"./.sperser_id.tmp
