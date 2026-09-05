// Query all CARTAOTOKNZD records
query cartaotoknzd verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
  guid = "Xb9g4pHsLwI8OOCeEVAg_zVMEeA"
}