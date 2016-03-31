# tts
curl -k -H "Authorization: Bearer 9c52fe4976ef4f069a450919edd6356a" -H "ocp-apim-subscription-key: 24391266-d12e-4f62-bb85-c1118fe4e6c2" -H "Accept-language: en-US" "https://api.api.ai/v1/tts?v=20150910&text=our+goal+is+to+make+the+process+of+creating+and+integrating+sophisticated+voice+interfaces+as+simple+as+possible" -o tts.wav
# SLU request
curl -H "Authorization: Bearer 9c52fe4976ef4f069a450919edd6356a" -H "ocp-apim-subscription-key: 24391266-d12e-4f62-bb85-c1118fe4e6c2" "https://api.api.ai/v1/query?v=20150910&query=hi+my+name+is+ray&lang=en"
