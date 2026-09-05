// Get AulaTeste record
query "aulateste/{aulateste_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int aulateste_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.aulateste_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
  guid = "nk2ZTF9xv7zzLeAxTpSuKpy3dRc"
}