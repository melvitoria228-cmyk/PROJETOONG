// Query all OE records
query oe verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $oe
  }

  response = $oe
  guid = "o0HPN1m3jILTKOQrvxaFM7B5uWE"
}