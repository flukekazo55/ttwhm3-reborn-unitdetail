import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { FactionGuide, FactionGuideApiData, GuideApiResponse } from '../../shared/models/guide.model';
import { toFactionGuide } from '../../shared/utils/guide-mapper';

@Injectable({ providedIn: 'root' })
export class KislevService {
  private readonly dataUrl = `${environment.apiUrl}/assets/data/kislev.json`;

  constructor(private http: HttpClient) {}

  getFaction(): Observable<FactionGuide> {
    return this.http
      .get<GuideApiResponse<FactionGuideApiData>>(this.dataUrl)
      .pipe(map((response) => this.toModel(response)));
  }

  private toModel(response: GuideApiResponse<FactionGuideApiData>): FactionGuide {
    if (!response.data) {
      throw new Error(response.error ?? 'Invalid KISLEV guide response');
    }
    return toFactionGuide(response.data.faction);
  }
}
