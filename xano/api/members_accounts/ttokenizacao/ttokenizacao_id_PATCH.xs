// Edit TTOKENIZACAO record
query "ttokenizacao/{ttokenizacao_id}" verb=PATCH {
  api_group = "Members & Accounts"

  input {
    int ttokenizacao_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.ttokenizacao_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $ttokenizacao
  }

  response = $ttokenizacao
  guid = "fFRWcruJ3k_EhpgWacbugZmAjS8"
}