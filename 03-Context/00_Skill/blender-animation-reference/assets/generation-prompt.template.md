Transform the supplied texture-free motion reference into {{requested_style}}. Generate exactly {{duration_seconds}} seconds at {{aspect_ratio}}. Preserve measured camera/subject movement, geometry relationships, timing, first view and final view.

Input roles: {{motion_video}} controls motion/geometry; {{first_frame}} and {{last_frame}} define matching boundary views; {{appearance_inputs}} supply appearance only. {{visibility_aid_explanation_if_applicable}}

Scene: {{explicit_subjects_shapes_positions_attachments_foreground_background_and_continuity}}

Execute this sequence exactly as authored, including any specified cuts or holds:

{{output_local_timed_blocks_with_start_camera_and_subject_motion_fixed_parts_visible_cues_endpoint_and_transition}}

Required ending: {{observable_framing_proximity_landmarks_subject_state_and_authored_hold_if_any}}

Finishing: {{materials_lighting_environment_and_requested_style_without_changing_motion}}

Preserve {{scene_specific_invariants}}. Avoid {{specific_failure_modes_without_contradicting_authored_action}}.

Time markers describe continuous progression, not pauses, unless a hold is specified. Prioritize reference choreography/event timing over additional cinematic actions.
