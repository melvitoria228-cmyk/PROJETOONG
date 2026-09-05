// Delete TTOKENIZACAO record.
query "ttokenizacao/{ttokenizacao_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int ttokenizacao_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.ttokenizacao_id
    }
  }

  response = null
  guid = "tuW282BM7JfA_FZe1Xi7AvFxc98"
}