import { Component, OnInit, Input,Output, EventEmitter} from '@angular/core';
import { Person } from '../models/Person';

@Component({
  selector: 'app-person-card',
  templateUrl: './person-card.component.html',
  styleUrls: ['./person-card.component.scss']
})
export class PersonCardComponent implements OnInit {
  @Input() person!: Person;
  editing: boolean = false;
  tmpName?: string;
  @Output() callDeleteEvent = new EventEmitter<number>();
  @Output() editStartedEvent = new EventEmitter<void>();
  @Output() editEndedEvent = new EventEmitter<void>();

  constructor() { }


  ngOnInit(): void {
  }

  editEnded():void{
    this.editing = false;
    this.editEndedEvent.emit();
  }

  onKey(event: any) {
    //handler for input field
    this.tmpName = event.target.value;
  }

  onEdit(){
    this.editing = true;
    this.editStartedEvent.emit();
  }

  onCancel()
  {
    this.editEnded();
  }

  onModify()
  {
    // tmpName-t validálni!
    if (!this.tmpName)
    {
      return;
    }
    this.person.name = this.tmpName;
    this.editEnded();

    fetch('http://localhost:8080/rename-person', {
              body: JSON.stringify({
                  id: this.person.id,
                  new_name: this.tmpName
              }),
              headers: {
                  'Content-Type': 'application/json'
              },
              method: 'POST'
          });
  }

  onDelete()
  {
    this.callDeleteEvent.emit(this.person.id);
    fetch('http://localhost:8080/delete-person', {
              body: JSON.stringify({
                  id: this.person.id,
              }),
              headers: {
                  'Content-Type': 'application/json'
              },
              method: 'POST'
          });
  }
}
