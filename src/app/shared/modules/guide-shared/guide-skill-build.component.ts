import { Component, Input } from '@angular/core';
import { SkillBuild, SkillLevelPlan, SkillStage, SkillStep } from '../../models/guide.model';

@Component({
  selector: 'app-guide-skill-build',
  templateUrl: './guide-skill-build.component.html',
  styleUrl: './guide-skill-build.component.scss',
})
export class GuideSkillBuildComponent {
  @Input({ required: true }) build!: SkillBuild;
  @Input({ required: true }) accent = '#aaa';

  failedIcons = new Set<string>();

  onIconError(step: SkillStep): void {
    this.failedIcons.add(this.iconKey(step));
  }

  hasIconFailed(step: SkillStep): boolean {
    return this.failedIcons.has(this.iconKey(step));
  }

  trackStage(_: number, stage: SkillStage): string {
    return `${stage.key}-${stage.title}`;
  }

  trackStep(_: number, step: SkillStep): string {
    return `${step.order}-${step.name}`;
  }

  trackLevel(_: number, row: SkillLevelPlan): number {
    return row.level;
  }

  private iconKey(step: SkillStep): string {
    return `${step.order}-${step.name}`;
  }
}
