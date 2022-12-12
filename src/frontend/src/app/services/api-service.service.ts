import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import type { Observable } from 'rxjs';
import { Person } from '../models/Person';
import { GetPersonsResponse } from '../models/GetPersonsResponse';



@Injectable({
  providedIn: 'root'
})
export class ApiService {

  apiPrefix = 'http://localhost:8080'

  constructor(public readonly http: HttpClient) {}

  public getDummy(): Observable<Array<Person>> {
      return this.http.get<Array<Person>>(`${this.apiPrefix}/dummy`);
  }

  public getPersons(): Observable<GetPersonsResponse>{
    return this.http.get<GetPersonsResponse>(`${this.apiPrefix}/get-persons`)
  }
}
