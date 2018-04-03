import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

import { ConsoPage } from "../conso/conso";
import * as io from "socket.io-client";

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {

  socket = io.connect("http://192.168.81.157:3000", { transports: [ "websocket"] });
  datas;

  constructor(public navCtrl: NavController) {
    //fill_val();
  }

  ionViewDidLoad(){
    console.log(this.socket)
    let tv;
    let price;

    this.socket.on('connect', function(){

    });
    this.socket.on('value', function(data){
      this.datas = data;
      document.getElementById("whatage").innerText = Math.floor(this.datas.totale + 1) + " kW/h";
      price = this.datas.totale / 0.1467;
      document.getElementById("day_price").innerText = Math.floor(price) + " €";
    });
  }
  goToOtherPage() {
    this.navCtrl.push(ConsoPage)
  }
}
