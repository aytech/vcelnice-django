import { Component, OnInit } from '@angular/core';
import { LanguageService } from '../../services';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {
  public language: string;

  constructor(private languageService: LanguageService) {
  }

  ngOnInit() {
    this.language = this.languageService.default_locale;
    this.languageService.language.subscribe(language => {
      this.language = language;
    });
  }
}
