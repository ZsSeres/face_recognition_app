import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { BrowserModule } from '@angular/platform-browser';
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { faPlay, faStop,faCirclePlay,faCircleStop, faFaceSmileWink,faMaskFace,faFaceSmile,faUsersViewfinder,faGear,faPerson,faUsers,faEdit,faTrashCan,faCross,faCheck,faCancel} from '@fortawesome/free-solid-svg-icons';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WebCamComponent } from './web-cam/web-cam.component';
import { NgxSpinnerModule } from "ngx-spinner";
import { MainPageComponent } from './main-page/main-page.component';
import { HeaderComponent } from './header/header.component';
import { PersonCardComponent } from './person-card/person-card.component';
import { PersonManagerComponent } from './person-manager/person-manager.component';
import { ApiService} from './services/api-service.service';
import { HttpClientModule} from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    WebCamComponent,
    MainPageComponent,
    HeaderComponent,
    PersonCardComponent,
    PersonManagerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FontAwesomeModule,
    NgxSpinnerModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [ApiService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(library: FaIconLibrary) {
    library.addIcons(faPlay,faStop,faCirclePlay,faCircleStop,faFaceSmileWink,faMaskFace,faFaceSmile,faUsersViewfinder,faGear,faPerson,faUsers,faEdit,faTrashCan,faCross,faCheck,faCancel)
  }
}
