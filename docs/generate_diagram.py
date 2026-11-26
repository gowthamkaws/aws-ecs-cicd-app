"""Regenerates docs/architecture.png  (python generate_diagram.py, needs matplotlib)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10.5), dpi=130)
ax.set_xlim(0, 160); ax.set_ylim(-22, 100); ax.axis('off')

def box(x, y, w, h, title, sub='', fc='#fff', ec='#232f3e', tc='#232f3e', fs=11, subfs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=1.8))
    n = sub.count('\n') + 1 if sub else 0
    ax.text(x+w/2, y+h/2+(1.4+0.9*(n-1) if sub else 0), title, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)
    if sub: ax.text(x+w/2, y+h/2-1.6, sub, ha='center', va='center', fontsize=subfs, color='#444', linespacing=1.3)

def arr(p1, p2, color='#232f3e', ls='-'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=16, lw=1.9, color=color, linestyle=ls, shrinkA=0, shrinkB=0))

def num(x, y, n, color='#232f3e'):
    ax.text(x, y, str(n), ha='center', va='center', fontsize=10, fontweight='bold', color='white',
            bbox=dict(boxstyle='circle,pad=0.3', fc=color, ec='white', lw=1.2), zorder=10)

ax.text(80, 96, 'FastAPI on AWS ECS Fargate: keyless CI/CD architecture', ha='center', fontsize=16, fontweight='bold', color='#232f3e')

ax.add_patch(FancyBboxPatch((2, 24), 40, 58, boxstyle="round,pad=0.4,rounding_size=1.5", fc='#f4f6f8', ec='#8a94a0', lw=1.5, ls='--'))
ax.text(22, 78.5, 'GitHub', ha='center', fontsize=12, fontweight='bold', color='#555')
box(6, 62, 32, 9, 'Developer', 'git push to main')
box(6, 36, 32, 14, 'GitHub Actions', 'deploy.yml\nrequests OIDC token', fc='#e8f0fe', ec='#1a56db', tc='#1a56db')
arr((22, 62), (22, 50.6)); num(26.5, 56.3, 1)

ax.add_patch(FancyBboxPatch((50, 4), 108, 76, boxstyle="round,pad=0.4,rounding_size=1.5", fc='#fffaf3', ec='#ff9900', lw=2))
ax.text(104, 76.2, 'AWS Cloud  |  eu-north-1 (Stockholm)', ha='center', fontsize=12, fontweight='bold', color='#c77700')
box(55, 58, 24, 11, 'IAM Role', 'OIDC trust (GitHub repo)', fc='#fdecea', ec='#c0392b', tc='#c0392b')
box(55, 36, 24, 11, 'Amazon ECR', 'private image repo', fc='#e9f7ef', ec='#1e8449', tc='#1e8449')
box(55, 10, 24, 10, 'AWS Budgets', '$5 monthly alert', fc='#f5f5f5', ec='#666', tc='#444')
arr((38.4, 46), (54.6, 62), color='#c0392b'); num(45, 55.5, 2, '#c0392b')
arr((38.4, 41), (54.6, 41), color='#1a56db'); num(46.5, 43.6, 3, '#1a56db')

ax.add_patch(FancyBboxPatch((85, 10), 70, 60, boxstyle="round,pad=0.4,rounding_size=1.2", fc='#fff', ec='#6c3fb5', lw=1.6, ls='--'))
ax.text(120, 66, 'VPC', ha='center', fontsize=11, fontweight='bold', color='#6c3fb5')
box(89, 49, 24, 12, 'Application\nLoad Balancer', 'port 80 | alb-sg', fc='#f3ecfb', ec='#6c3fb5', tc='#6c3fb5', fs=10)
box(126, 40, 25, 24, 'ECS Fargate Service', 'python:3.12-slim\nFastAPI + Uvicorn :8000\necs-sg: only from alb-sg', fc='#fff3e0', ec='#e67e22', tc='#c0651a', fs=10.5)
box(89, 16, 24, 11, 'CloudWatch Logs', '/ecs/cloud-portfolio-task', fc='#eef7fb', ec='#117a8b', tc='#117a8b', fs=10.5, subfs=8)

box(89, 84, 24, 8, 'Internet users')
arr((101, 83.6), (101, 61.6)); num(105, 72, 6)
ax.text(108, 72, 'HTTP :80', fontsize=8.5, va='center')
arr((113.4, 55), (125.6, 55), color='#6c3fb5'); num(119.5, 58, 7, '#6c3fb5')
arr((79.4, 42), (125.6, 44), color='#1e8449'); num(100, 44.4, 5, '#1e8449')
arr((133, 39.6), (113.4, 23), color='#117a8b'); num(124, 30.5, 8, '#117a8b')

ax.plot([22, 22, 139, 139], [36, 0, 0, 10], color='#1a56db', lw=1.9, ls='--')
arr((139, 10), (139, 39.6), color='#1a56db', ls='--')
num(22, 18, 4, '#1a56db')

steps = [
 ('1', '#232f3e', 'Push to main triggers the GitHub Actions workflow'),
 ('2', '#c0392b', 'OIDC JWT exchanged for temporary credentials (no stored keys)'),
 ('3', '#1a56db', 'Docker image built and pushed to ECR, tagged with commit SHA'),
 ('4', '#1a56db', 'New task definition registered, ECS service updated'),
 ('5', '#1e8449', 'Fargate pulls the new image from ECR'),
 ('6', '#232f3e', 'Users reach the Application Load Balancer on port 80'),
 ('7', '#6c3fb5', 'ALB forwards to the task on port 8000, health check on /health'),
 ('8', '#117a8b', 'Container logs stream to CloudWatch Logs'),
]
y = -6
for i, (n, c, t) in enumerate(steps):
    x0 = 3 + (0 if i < 4 else 82)
    num(x0, y-(i % 4)*3.8, n, c)
    ax.text(x0+3, y-(i % 4)*3.8, t, fontsize=8.6, va='center', color='#222')

plt.savefig('architecture.png', bbox_inches='tight', facecolor='white')
