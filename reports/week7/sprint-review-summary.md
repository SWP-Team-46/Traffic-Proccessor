# Week 7 Meeting Summary – Sprint Review & Customer Handover

**Project:** Traffic-Processor (SWP-Team-46)  
**Sprint:** Sprint 5 (final)  
**Meeting Type:** Sprint Review / Customer Handover  
**Date:** Week 7 (July 13–19, 2026)  
**Status:** MVP v3 – Accepted with Follow-up Items


## 1. Meeting Overview

The Week 7 sprint review served as the final customer handover meeting for the Traffic-Processor project. The team demonstrated the current state of the product, discussed remaining limitations, and agreed on the acceptance status. The customer formally accepted the product **with follow-up items** rather than full acceptance, indicating that while the core functionality is working, several improvements are required before production deployment.


## 2. Sprint Context

**Sprint 5 Goal:** Finalise MVP v3 and prepare for customer handover  
**Sprint Dates:** 13 July 2026 – 19 July 2026 (follow-up to Sprint 4)  

**Previous Sprint (Week 6) outcomes:**  
- Separated CNSS and TP startup  
- Website UI overhaul  
- Total Sprint 4 story points: 13  
- Customer feedback noted that the README was sparse, but other parts were acceptable  
- Planned Week 7 follow-up: bug fixes, add data storage, try to add VM-to-VM compatibility


## 3. Key Discussion Points

### 3.1 Product Demonstration

The team walked through the current system, which is fully containerised and includes TProc, CNSS, and PostgreSQL. The demonstration covered:

- **Bitrate testing** – the team tested pre-downloaded videos at 8 Mbps, 40 Mbps, and 100 Mbps to observe packet size behaviour under different bitrates
- **Network activity monitoring** – the system collects traffic between the backend and TP, with visible activity from both the target and the monitoring system itself

### 3.2 Technical Limitations Discussed

**Encryption & Network Protocols** – The system encrypts traffic to avoid detection; however, this means that with significant lag. This limitation was noted as inherent to the approach rather than a bug.

**Database Reset Functionality** – The reset command does not currently work with the database because it has not been updated for the new version. The customer questioned the purpose of clearing the database, noting that this would result in loss of collected user data—equivalent to a malicious data deletion scenario. The team acknowledged this and agreed to reconsider the approach.

**Data Attribution by Container** – When multiple processors run simultaneously, all data is currently summed together. The customer recommended that data should be tagged at the database level with either the processor ID or container identifier. This would allow the UI to filter and display data per container.

### 3.3 Deployment & Access

- The `traffic-poster` module is pulled from the Docker cloud – the team has pushed the image and only the correct command is needed to run it  
- The `help` command in the command line is the most up-to-date source of information  
- Documentation will be updated to reflect the latest deployment changes

### 3.4 Acceptance Decision

The customer was asked to choose from three categories:
1. **Accepted**
2. **Accepted with follow-up items**
3. **Not yet accepted**

The customer selected **"Accepted with follow-up items"**, indicating that the product is fundamentally working but requires additional work before full production readiness.


## 4. Follow-up Items Identified

| # | Follow-up Item | Priority | Owner |
|---|----------------|----------|-------|
| 1 | **Data attribution by container** – Implement tagging of data at the database level with processor/container ID to allow per-container filtering in the UI | High | TBD |
| 2 | **Database reset handling** – Either fix the reset functionality for the new version or remove/replace it with a time-window based approach | Medium | TBD |
| 3 | **Update documentation** – Ensure all deployment documentation is current and aligns with the latest changes | Medium | Team |
| 4 | **VM-to-VM compatibility** – Continue work on adding cross-VM support | Low | TBD |


## 5. Product Status Summary

**Current State:**
- System is fully containerised and operational  
- Core functionality is working  
- All documented User Acceptance Tests (UATs) have passed  

**Known Limitations:**
- Reset command does not work with the database  
- Data from multiple containers is aggregated rather than separated  
- Traficoster does not work correctly under significant network lag  

**Readiness for Production:**
- The product is **ready for the deployed use** but not yet polished 
- Follow-up items must be addressed for effective use


## 6. Team Contributions (Week 7)

Based on the Week 6 traceability and the Week 7 meeting context:

| Team Member | Role in Week 7 |
|-------------|----------------|
| mrZom49 | Sprint coordination, documentation updates, integration management |
| TimLih-h | Deployment simplification, bug fixes |
| jan-ajata | Frontend improvements |
| inseeee | Dashboard theme work |
| LimpingCoronation | Retrospective and reflection documentation |


## 7. Next Steps

1. Address the follow-up items identified during the review
2. Update the documentation to reflect the latest deployment process
3. Prepare final handover documentation

---

*This summary was compiled from the Week 7 sprint review transcript and previous sprint reports (Weeks 5–6) available in the project repository.*
