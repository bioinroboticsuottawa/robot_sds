# remove all the '{' and '}'

# create dialog
curl -X POST -F "file=@{foo_app.xml}" -F "name={foo_app}" https://gateway.watsonplatform.net/dialog/api/v1/dialogs -u "{username}:{password}"
# delete dialog
curl -X DELETE -u "username:password" "https://gateway.watsonplatform.net/dialog/api/v1/dialogs/{dialog_id}"
