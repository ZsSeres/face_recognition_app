import { Injectable } from '@angular/core';
import { BehaviorSubject, combineLatest, interval, ReplaySubject, startWith } from 'rxjs';
import { GetPersonsResponse } from '../models/GetPersonsResponse';
import { Person } from '../models/Person';
import { ApiService } from './api-service.service';

@Injectable({
  providedIn: 'root'
})
export class PersonsService {

  autoRefresh$ = interval(1000).pipe(startWith(0));
  refreshToken$: BehaviorSubject<undefined> = new BehaviorSubject(undefined);

  // state: ReplaySubject<object> = new ReplaySubject<object>(2, 100000);
  persons: ReplaySubject<Array<Person>> = new ReplaySubject<Array<Person>>(2, 100000);
  connectionError$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  constructor(private readonly apiService: ApiService) { this.startWatching(); }

  startWatching(): void {
    combineLatest([this.autoRefresh$, this.refreshToken$]).subscribe(()=>{
      // this.getData();
      this.getPersons();
    })
  }

  // getData(): void {
  //   this.apiService.getDummy().subscribe( {
  //     next: (data:object) => {
  //       this.state.next(data);
  //       this.connectionError$.next(false);
  //     },
  //     error: () => { this.connectionError$.next(true) }})
  // }

  getPersons(): void {
    this.apiService.getPersons().subscribe( {
      next: (personsResponse: GetPersonsResponse) => {
        this.persons.next(personsResponse.persons);
        this.connectionError$.next(false);
      },
      error: () => { this.connectionError$.next(true) }})
  }

}
