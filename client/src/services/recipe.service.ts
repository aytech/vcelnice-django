import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiConstants } from 'config';
import { Recipe } from 'interfaces';

@Injectable()
export class RecipeService {

  constructor(
    private http: HttpClient
  ) {
  }

  getRecipes(): Observable<Array<Recipe>> {
    return this.http.get<Recipe[]>(ApiConstants.GET_RECIPES);
  }
}
