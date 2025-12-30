import {
  Component,
  OnInit
} from '@angular/core';
import {
  ActivatedRoute,
  Params
} from '@angular/router';
import { LanguageService } from '../services';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    standalone: false
})
export class AppComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private languageService: LanguageService) {
  }

  ngOnInit() {
    if (this.route.snapshot.queryParams.locale !== undefined) {
      this.languageService.setLanguage(this.route.snapshot.queryParams.locale);
    }
    this.route.queryParams.subscribe((params: Params) => {
      if (params.locale !== undefined) {
        this.languageService.setLanguage(params.locale);
      }
    });
  }
}
