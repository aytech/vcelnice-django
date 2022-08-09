import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './home/home.component';
import { PhotoComponent } from './photo/photo.component';
import { VideoComponent } from './video/video.component';
import { CertificatesComponent } from './certificates/certificates.component';
import { RegionComponent } from './region/region.component';
import { ModalComponent } from './modal/modal.component';
import { NewsComponent } from './news/news.component';
import { RecipesComponent } from './recipes/recipes.component';
import { PricesComponent } from './prices/prices.component';
import { ReservationComponent } from './prices/prices.component';
import { ContactComponent, ContactModalComponent } from './contact/contact.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { PrivacyComponent } from './privacy/privacy.component';
import {
  CertificateService,
  ContactService,
  GenericService,
  HomeService,
  LanguageService,
  NewsService,
  PhotoService,
  PriceService,
  RecipeService,
  VideoService
} from 'services';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PhotoComponent,
    VideoComponent,
    CertificatesComponent,
    RegionComponent,
    ModalComponent,
    NewsComponent,
    RecipesComponent,
    PricesComponent,
    ReservationComponent,
    ContactComponent,
    ContactModalComponent,
    PageNotFoundComponent,
    NavbarComponent,
    FooterComponent,
    PrivacyComponent
  ],
  imports: [
    FontAwesomeModule,
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule
  ],
  bootstrap: [
    AppComponent
  ],
  providers: [
    CertificateService,
    ContactService,
    GenericService,
    HomeService,
    LanguageService,
    NewsService,
    PhotoService,
    PriceService,
    RecipeService,
    VideoService
  ],
  exports: [ PrivacyComponent ]
})
export class AppModule {
}
