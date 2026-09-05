// Delete STATUS_TTOKENIZACAO record.
query "status_ttokenizacao/{status_ttokenizacao_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int status_ttokenizacao_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_ttokenizacao_id
    }
  }

  response = null
  guid = "A-Km5USr0JRMXBc9x-M1wiUnHAU"
}