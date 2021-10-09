endpointURL = 'https://plfxt603af.execute-api.us-east-2.amazonaws.com/prod/'

// // Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', endpointURL, true)

request.onload = function () {
  var data = JSON.parse(this.response)
  // console.log(data)
  var donutCleanList = []

  for (let i = 0; i < data.length; i++) {
    
    var donutName = data[i][1]["stringValue"]
    
    var donutUrl = data[i][2]["stringValue"]

    // convert string into array
    var donutTypeList = JSON.parse(data[i][3]["stringValue"])

    // convert to string for div attribute
    var donutTypeString = ""
    for (let i = 0; i < donutTypeList.length; i++) {
      donutTypeString = donutTypeString + " " + donutTypeList[i]
    }

    var donutRow = [donutName, donutUrl, donutTypeString]

    donutCleanList.push(donutRow)

  } 

  // find how many rows we need for the list
  var quotient = Math.floor(donutCleanList.length/3);
  var remainder = donutCleanList.length % 3;

  for (let i = 0; i < ((quotient+remainder)*3); i = i + 3) {
    try{
      item1 = donutCleanList[i]
    } catch {
      item1 = ""
      console.log("no item 1")
    }
    try{
      item2 = donutCleanList[i+1]
      if (item2 == undefined) {
        item2 = ["", "", ""]
      }
    } catch {
      item2 = ""
      console.log("no item 2")
    }
    try{
      item3 = donutCleanList[i+2]
      if (item3 == undefined) {
        item3 = ["", "", ""]
      }
    } catch {
      item3 = ""
      console.log("no item 3")
    }

    divText = `
    <div class="row align-items-center">
        <div class="col" id="${item1[2]}">
          <img src="${item1[1]}" alt="" width="310">
          <div class="donutNameStyle">${item1[0]}</div>
        </div>
        <div class="col" id="${item2[2]}">
          <img src="${item2[1]}" alt="" width="310">
          <div class="donutNameStyle">${item2[0]}</div>
        </div>
        <div class="col" id="${item3[2]}">
          <img src="${item3[1]}" alt="" width="310">
          <div class="donutNameStyle">${item3[0]}</div>
        </div>
      </div>
    `
    console.log(divText)

    document.getElementById("donutContainer").innerHTML += divText
  }
}

// Send request
request.send()
 







