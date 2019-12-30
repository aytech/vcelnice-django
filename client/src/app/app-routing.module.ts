import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { PhotoComponent } from './photo/photo.component';
import { VideoComponent } from './video/video.component';
import { CertificatesComponent } from './certificates/certificates.component';
import { RegionComponent } from './region/region.component';
import { NewsComponent } from './news/news.component';
import { RecipesComponent } from './recipes/recipes.component';
import { PricesComponent } from './prices/prices.component';
import { ContactComponent } from './contact/contact.component';
import { PrivacyComponent } from './privacy/privacy.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'foto', component: PhotoComponent },
  { path: 'video', component: VideoComponent },
  { path: 'certifikaty', component: CertificatesComponent },
  { path: 'region', component: RegionComponent },
  { path: 'novinky', component: NewsComponent },
  { path: 'recepty', component: RecipesComponent },
  { path: 'cenik', component: PricesComponent },
  { path: 'kontakt', component: ContactComponent },
  { path: 'privacy', component: PrivacyComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  exports: [
    RouterModule
  ],
  imports: [
    RouterModule.forRoot(routes)
  ]
})
export class AppRoutingModule { }
