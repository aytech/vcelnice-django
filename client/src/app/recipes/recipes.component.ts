import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { RecipeService } from 'services';
import { Recipe } from 'interfaces';

@Component({
    selector: 'app-recipees',
    templateUrl: './recipes.component.html',
    styleUrls: ['./recipes.component.css'],
    standalone: false
})
export class RecipesComponent implements OnInit {

  public recipes: Array<Recipe>;
  public loading: boolean;

  constructor(private recipeService: RecipeService) {
    this.loading = true;
    this.recipes = [];
  }

  ngOnInit() {
    this.recipeService.getRecipes()
      .subscribe((response: Recipe[]) => {
        this.loading = false;
        this.recipes = response;
      }, (error: HttpErrorResponse) => {
        this.loading = false;
        console.error('Error fetching data: ', error.statusText);
      });
  }
}
