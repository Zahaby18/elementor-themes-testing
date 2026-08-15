<?php
/**
 * Plugin Name: Agenzy Demo Posts
 * Description: Generate 10 demo blog posts + featured images for the Agenzy template kit. Activate, then deactivate & delete this plugin — the posts stay.
 * Version: 1.0.0
 * Author: Agenzy
 * Requires at least: 5.8
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Generate demo posts on activation (only once).
 */
function agenzy_demo_posts_activate() {
	if ( get_option( 'agenzy_demo_posts_done' ) ) {
		return;
	}

	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';

	$IMG = 'https://cdn.jsdelivr.net/gh/Zahaby18/elementor-themes-testing@main/assets/img/';

	$posts = [
		[
			'title'   => '10 Conversion Lessons from 100+ Landing Pages',
			'img'     => 'img07.jpg',
			'excerpt' => 'We analyzed the patterns that separate high-converting landing pages from the rest. Here is what actually works.',
			'content' => "<p>Over the last year we audited more than a hundred landing pages across industries — and the results were remarkably consistent. The pages that convert share a handful of traits: a single clear headline, one primary call to action, social proof placed early, and a friction-free form.</p><p>The pages that don't convert tend to try to do too much at once. Multiple competing CTAs, vague headlines, and walls of text are the usual culprits. In this post we break down the ten lessons that moved the needle most for our clients.</p>",
		],
		[
			'title'   => 'The Design System That Cut Our Build Time in Half',
			'img'     => 'img08.jpg',
			'excerpt' => 'How we standardized components, tokens, and handoff — and why your team should too.',
			'content' => "<p>Six months ago our build process was slowing us down. Every new page started from scratch, and small inconsistencies crept into every project. Then we built a design system — a shared library of tokens, components, and guidelines.</p><p>The result: we ship landing pages roughly twice as fast, and every deliverable is visually consistent. Here is exactly how we structured it, and the mistakes we made along the way.</p>",
		],
		[
			'title'   => 'SEO in 2026: What Still Matters (and What Doesn’t)',
			'img'     => 'img09.jpg',
			'excerpt' => 'Algorithm changes come and go. These fundamentals have survived every update so far.',
			'content' => "<p>SEO advice ages badly. Tactics that worked three years ago can hurt you today. But underneath all the noise, a few fundamentals have survived every algorithm update since the beginning.</p><p>In this guide we separate the evergreen principles from the passing fads, and show you where to focus your effort in 2026.</p>",
		],
		[
			'title'   => 'How We Rebranded a Fintech Startup in 30 Days',
			'img'     => 'img10.jpg',
			'excerpt' => 'A tight timeline, a total visual refresh, and a launch that didn’t miss. Here’s how we did it.',
			'content' => "<p>When a fast-growing fintech client asked for a complete rebrand in a month, we knew the process had to be ruthlessly efficient. No endless mood boards, no committee sign-offs — just a clear plan and fast decisions.</p><p>Here is the exact timeline we followed, from the first workshop to the launch-day deploy.</p>",
		],
		[
			'title'   => 'From Zero to 10K Visitors: Our Content Playbook',
			'img'     => 'img11.jpg',
			'excerpt' => 'The publishing rhythm, formats, and distribution habits that grew organic traffic for a B2B client.',
			'content' => "<p>Content marketing often fails because it’s treated as a side project. We treat it as a product. For one B2B client we built a publishing engine that took them from zero to ten thousand monthly visitors in under a year.</p><p>This post walks through the playbook: topic clusters, a realistic cadence, and the distribution habits that made it stick.</p>",
		],
		[
			'title'   => 'Why Your Website Load Time Is Costing You Clients',
			'img'     => 'img12.jpg',
			'excerpt' => 'Every extra second of load time quietly erodes trust — and revenue. Here’s what to fix first.',
			'content' => "<p>Slow websites don’t just frustrate visitors — they actively push people toward your competitors. Studies consistently show that load time has a direct impact on conversion and bounce rate.</p><p>We look at the most common causes of slow pages and the fixes that deliver the biggest gains for the least effort.</p>",
		],
		[
			'title'   => 'The Anatomy of a High-Performing Team',
			'img'     => 'img13.jpg',
			'excerpt' => 'What separates teams that consistently ship from teams that consistently stall.',
			'content' => "<p>Great teams aren’t an accident. After years of working with in-house and distributed teams, we’ve noticed clear patterns in the ones that consistently deliver.</p><p>Here’s the anatomy: how they communicate, how they scope work, and how they handle the inevitable scope creep.</p>",
		],
		[
			'title'   => '5 UI Patterns That Are Secretly Hurting Your Conversion',
			'img'     => 'img14.jpg',
			'excerpt' => 'These design choices feel polished but quietly push users away.',
			'content' => "<p>Some UI patterns look modern but work against you. Hidden navigation, aggressive pop-ups, and low-contrast text are just a few of the offenders we regularly remove during redesigns.</p><p>We break down five patterns to audit on your own site, and what to replace them with.</p>",
		],
		[
			'title'   => 'WordPress vs Custom Build: What We Tell Our Clients',
			'img'     => 'img15.jpg',
			'excerpt' => 'The honest answer: it depends. Here’s how we help clients choose.',
			'content' => "<p>Every client eventually asks us the same question: should we use WordPress or build something custom? The answer is rarely black and white.</p><p>In this post we share the framework we use to evaluate the trade-offs — cost, speed, flexibility, and who will maintain it long-term.</p>",
		],
		[
			'title'   => 'A Beginner’s Guide to Accessibility in Web Design',
			'img'     => 'img16.jpg',
			'excerpt' => 'Accessibility isn’t optional — and it’s easier to start than you think.',
			'content' => "<p>Accessibility is often treated as an afterthought, but it should be a foundation. Beyond the ethical argument, accessible websites simply work better for everyone — including search engines.</p><p>This beginner-friendly guide covers the basics: contrast, focus states, semantic structure, and the tools we use to test our work.</p>",
		],
	];

	$created = 0;
	foreach ( $posts as $p ) {
		$post_id = wp_insert_post( [
			'post_title'    => $p['title'],
			'post_content'  => $p['content'],
			'post_excerpt'  => $p['excerpt'],
			'post_status'   => 'publish',
			'post_type'     => 'post',
			'post_category' => [ 1 ],
		] );

		if ( is_wp_error( $post_id ) ) {
			continue;
		}

		$attachment_id = media_sideload_image( $IMG . $p['img'], $post_id, null, 'id' );
		if ( ! is_wp_error( $attachment_id ) ) {
			set_post_thumbnail( $post_id, $attachment_id );
		}
		$created++;
	}

	update_option( 'agenzy_demo_posts_done', 1 );
	set_transient( 'agenzy_demo_posts_notice', $created, 60 );
}
register_activation_hook( __FILE__, 'agenzy_demo_posts_activate' );

/**
 * Show an admin notice after generation.
 */
function agenzy_demo_posts_notice() {
	$count = get_transient( 'agenzy_demo_posts_notice' );
	if ( false === $count ) {
		return;
	}
	echo '<div class="notice notice-success is-dismissible"><p><strong>Agenzy Demo Posts:</strong> ' . (int) $count . ' demo posts created with featured images. You can now deactivate &amp; delete this plugin — the posts will stay.</p></div>';
}
add_action( 'admin_notices', 'agenzy_demo_posts_notice' );
