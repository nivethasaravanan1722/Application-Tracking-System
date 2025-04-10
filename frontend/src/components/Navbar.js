'use client'

import { useState } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Dashboard', href: '#' },
  { name: 'Upload Resume', href: '#upload' },
  { name: 'Leaderboard', href: '#leaderboard' },
  { name: 'Recommendations', href: '#recommendations' },
]

export default function ATSNavbarHero() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="relative">
      {/* Navbar */}
      <header className="fixed inset-x-0 top-0 z-50 backdrop-blur-md bg-white/10">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1 items-center">
            <a href="#" className="-m-1.5 p-1.5 flex items-center space-x-2">
              {/* <img src="/assets/ats-logo.png" alt="ATS Logo" className="h-8 w-auto" /> */}
              <span className="text-yellow-200 font-bold text-lg">ATS Pro</span>
            </a>
          </div>
          <div className="flex lg:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-white"
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
          </div>
          <div className="hidden lg:flex lg:gap-x-12">
            {navigation.map((item) => (
              <a 
                key={item.name} 
                href={item.href} 
                className="text-sm font-medium text-white hover:underline hover:underline-offset-4 hover:decoration-2"
              >
                {item.name}
              </a>
            ))}
          </div>
          <div className="hidden lg:flex lg:flex-1 lg:justify-end lg:items-center lg:gap-4">
            <a 
              href="#login" 
              className="text-sm font-semibold text-white hover:text-gray-300 transition-colors"
            >
              Log in
            </a>
            <a
              href="#signup"
              className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 transition-colors"
            >
              Sign up
            </a>
          </div>
        </nav>

        {/* Mobile Dialog */}
        <Dialog open={mobileMenuOpen} onClose={setMobileMenuOpen} className="lg:hidden">
          <div className="fixed inset-0 z-50" />
          <DialogPanel className="fixed inset-y-0 right-0 z-50 w-full bg-white px-6 py-6 sm:max-w-sm">
            <div className="flex items-center justify-between">
              <a href="#" className="-m-1.5 p-1.5">
                <img src="/assets/ats-logo.png" alt="ATS" className="h-8 w-auto" />
              </a>
              <button
                type="button"
                onClick={() => setMobileMenuOpen(false)}
                className="-m-2.5 rounded-md p-2.5 text-gray-700"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            <div className="mt-6 space-y-2">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-900 hover:bg-gray-100"
                >
                  {item.name}
                </a>
              ))}
              <div className="pt-4 space-y-2 border-t border-gray-200">
                <a
                  href="#login"
                  className="block rounded-lg px-3 py-2.5 text-base font-medium text-gray-900 hover:bg-gray-100"
                >
                  Log in
                </a>
                <a
                  href="#signup"
                  className="block rounded-lg px-3 py-2.5 text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Sign up
                </a>
              </div>
            </div>
          </DialogPanel>
        </Dialog>
      </header>

      {/* Hero Section */}
      <div className="relative isolate overflow-hidden bg-gradient-to-tr from-gray-900 via-blue-900 to-black min-h-screen flex flex-col justify-between pt-32 pb-20 px-4 sm:px-6">
        {/* Main Hero Content */}
        <div className="mx-auto max-w-2xl text-center text-white">
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            Smarter Hiring with AI-Powered Resume Analysis
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-300">
            Upload resumes, get AI-based candidate scoring, view skill charts, and streamline your selection process.
          </p>
        </div>
        
        {/* Action Buttons */}
        <div className="mx-auto max-w-2xl space-y-6 text-center">
          <div>
            <a
              href="#upload"
              className="inline-block rounded-md bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow hover:bg-indigo-500 transition-colors"
            >
              Upload Resume
            </a>
          </div>
          <div>
            <a
              href="#leaderboard"
              className="inline-block rounded-md border border-white px-6 py-3.5 text-sm font-semibold text-white hover:bg-white hover:text-gray-900 transition-colors"
            >
              View Leaderboard
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}