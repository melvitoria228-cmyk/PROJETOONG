// Delete PAPEL record.
query "papel/{papel_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int papel_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.papel_id
    }
  }

  response = null
  guid = "GmURPWdHXNVXQ8RxTumim4fQv1g"
}