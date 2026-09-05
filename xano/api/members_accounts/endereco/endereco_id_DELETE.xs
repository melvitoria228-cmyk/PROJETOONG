// Delete ENDERECO record.
query "endereco/{endereco_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int endereco_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.endereco_id
    }
  }

  response = null
  guid = "9iGj2T9QyB4nP0gNFJ0PT51stEU"
}