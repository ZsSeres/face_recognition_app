import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebCamComponent } from './web-cam.component';

describe('WebCamComponent', () => {
  let component: WebCamComponent;
  let fixture: ComponentFixture<WebCamComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WebCamComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WebCamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
