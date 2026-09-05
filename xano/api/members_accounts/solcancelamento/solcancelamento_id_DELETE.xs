// Delete SOLCANCELAMENTO record.
query "solcancelamento/{solcancelamento_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int solcancelamento_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.solcancelamento_id
    }
  }

  response = null
  guid = "BU6RayhUNPPenmGCtWRu8t0S7LU"
}