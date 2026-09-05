// Get TESTORNO record
query "testorno/{testorno_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int testorno_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.testorno_id
    } as $testorno
  
    precondition ($testorno != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $testorno
  guid = "CqdjsT_q2QP9lLcFUMMRkrflNrA"
}