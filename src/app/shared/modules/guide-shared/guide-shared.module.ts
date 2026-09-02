import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { TagModule } from 'primeng/tag';
import { GuideFactionComponent } from './guide-faction.component';
import { GuideLordComponent } from './guide-lord.component';
import { GuideSkillBuildComponent } from './guide-skill-build.component';
import { GuideUnitCardComponent } from './guide-unit-card.component';

@NgModule({
  declarations: [
    GuideFactionComponent,
    GuideLordComponent,
    GuideSkillBuildComponent,
    GuideUnitCardComponent,
  ],
  imports: [CommonModule, TagModule],
  exports: [
    GuideFactionComponent,
    GuideLordComponent,
    GuideSkillBuildComponent,
    GuideUnitCardComponent,
  ],
})
export class GuideSharedModule {}
