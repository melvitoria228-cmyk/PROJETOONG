// Add STATUS_TESTORNO record
query status_testorno verb=POST {
  api_group = "Members & Accounts"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_testorno
  }

  response = $status_testorno
  guid = "RI5yWEFKtw8sNFJGvbOfKvz_VMs"
}