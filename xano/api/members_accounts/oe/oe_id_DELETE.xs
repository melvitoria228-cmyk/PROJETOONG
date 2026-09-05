// Delete OE record.
query "oe/{oe_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int oe_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.oe_id
    }
  }

  response = null
  guid = "o-DHf2gDTMyykja2GSl90tWKtCk"
}