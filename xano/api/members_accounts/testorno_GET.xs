// Query all TESTORNO records
query testorno verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $testorno
  }

  response = $testorno
  guid = "RoscggqnmF5L2pGbWAsfZgFP3j0"
}