import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonManagerComponent } from './person-manager.component';

describe('PersonManagerComponent', () => {
  let component: PersonManagerComponent;
  let fixture: ComponentFixture<PersonManagerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PersonManagerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PersonManagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
