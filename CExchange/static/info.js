function changecontent() {
    let x = document.forms["infoform"]["info"].value;
    if (x == "Bitcoin") {
        document.getElementById("content").innerHTML = document.getElementById("BitcoinText").innerHTML;
        document.getElementById("web").href = "https://bitcoin.org/en/";
        document.getElementById("web").innerHTML = "Bitcoin Official Website";
    }
    else if (x == "Litecoin") {
        document.getElementById("content").innerHTML = document.getElementById("LitecoinText").innerHTML;
        document.getElementById("web").href = "https://litecoin.com/en/";
        document.getElementById("web").innerHTML = "Litecoin Official Website";
    }
    else if (x == "Dash") {
        document.getElementById("content").innerHTML = document.getElementById("DashText").innerHTML;
        document.getElementById("web").href = "https://www.dash.org/";
        document.getElementById("web").innerHTML = "Dash Official Website";
    }
    else if (x == "BitcoinCash") {
        document.getElementById("content").innerHTML = document.getElementById("BitcoinCashText").innerHTML;
        document.getElementById("web").href = "https://bitcoincash.org/";
        document.getElementById("web").innerHTML = "BitcoinCash Official Website";
    }
    else if (x == "platform") {
        document.getElementById("content").innerHTML = document.getElementById("platformText").innerHTML;
        document.getElementById("web").href = "";
        document.getElementById("web").innerHTML = "";
    }
}