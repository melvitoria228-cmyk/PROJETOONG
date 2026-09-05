// Query all STATUS_TESTORNO records
query status_testorno verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $status_testorno
  }

  response = $status_testorno
  guid = "SZgM5GYPejhdMOlvpKnaOlKu_ZU"
}