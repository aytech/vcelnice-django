import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Event, NavigationEnd, Router } from '@angular/router';
import { LanguageService } from '../../services';
import { Culture } from '../../interfaces';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  @ViewChild('navbarToggle') navbarToggle: ElementRef;
  @ViewChild('menu') menu: ElementRef;
  public locale: string;
  public cultures: Culture;

  constructor(private router: Router, private languageService: LanguageService) {
  }

  private isMenuOpen(): boolean {
    return this.menu.nativeElement.offsetParent !== null;
  }

  ngOnInit() {
    this.locale = this.languageService.locale;
    this.cultures = this.languageService.cultures;
    this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        if (this.isMenuOpen()) {
          this.navbarToggle.nativeElement.click();
        }
      }
    });
    this.languageService.language.subscribe(() => {
      this.locale = this.languageService.locale;
      this.cultures = this.languageService.cultures;
    });
  }
}
