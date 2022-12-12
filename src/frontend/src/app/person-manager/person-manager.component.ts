import { Component, OnInit } from '@angular/core';
import {Person} from "../models/Person";
import {Face} from "../models/Face";
import { ApiService } from '../services/api-service.service';
import { PersonsService } from '../services/persons.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-person-manager',
  templateUrl: './person-manager.component.html',
  styleUrls: ['./person-manager.component.scss']
})
export class PersonManagerComponent implements OnInit {
  persons!: Array<Person>
  personsWatch!: Subscription;
  editNumber: number = 0; //number of cards that is being editing
  //only allow update if this number is zero!
  //this stops the refresh while some element is being edited

  constructor(private readonly apiService: ApiService,private personsService: PersonsService) {
    // const face1: Face = {id:1,images_file_path:"assets/Domestic_cat.jpg"};
    // const person1: Person = {id:1,name:"Mirci",faces:[face1]};
    // const face2: Face = {id:1,images_file_path:"assets/cat.png"};
    // const person2: Person = {id:1,name:"Hópihe",faces:[face2]};
    // this.persons = [person1,person2,person2,person2,person2,person2,person2];
    this.apiService = apiService;
    this.personsService = personsService;
   }

  ngOnInit(): void {
    this.apiService.getDummy().subscribe((message)=>{
      console.log(message);
    })
    this.personsWatch = this.personsService.persons.subscribe(
      (message)=>{console.log(message)})
    this.personsService.persons.subscribe((persons)=>{
      if (this.editNumber == 0)
      {
        this.persons = persons
      }

    })
  }
  deletePerson(id:number):void{
    const indexOfObject = this.persons.findIndex((person) => {
      return person.id === id;
    });

    console.log(indexOfObject.toString());
    if (indexOfObject !== -1) {
      this.persons.splice(indexOfObject, 1);
    }
  }

  startedEditing(evt:void):void{
    //Called when one card is being edited
    console.log("Someone started editing")
    this.editNumber++;
    console.log(this.editNumber);
  }

  endEditing(evt:void):void{
    //Called when one card is no longer edited.
    console.log("Someone finished editing")
    if(this.editNumber==0)
    {
      return;
    }
    this.editNumber--;
    console.log(this.editNumber);
  }
}
