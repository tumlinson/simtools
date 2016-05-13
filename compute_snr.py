import numpy as np

def compute_snr(aperture, exposure_in_hours, ab_magnitudes):
    # this will be a plain python function that will produce the SNR numbers

    diff_limit = 1.22*(500.*0.000000001)*206264.8062/aperture
    print 'diff_limit', diff_limit

    pixel_size = np.array([0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.016, 0.04, 0.04, 0.04]) 

    source_magnitudes = np.array([1., 1., 1., 1., 1., 1., 1.]) * ab_magnitudes
    central_wavelength = np.array([155., 228., 360., 440., 550., 640., 790., 1260., 1600., 2220.])
    ab_zeropoint = np.array([35548., 24166., 15305., 12523., 10018., 8609., 6975., 4373., 3444., 2482.])
    total_qe = np.array([0.1, 0.1, 0.15, 0.45, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
    aperture_correction = np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    bandpass_r = np.array([5., 5., 5., 5., 5., 5., 5., 5., 5., 5.])
    derived_bandpass = central_wavelength / bandpass_r
    # two efficiency factors omitted

    detector_read_noise = np.array([3., 3., 3., 3., 3., 3., 3., 4., 4., 4.])
    dark_current = np.array([0.0005, 0.0005, 0.001, 0.001, 0.001, 0.001, 0.001, 0.002, 0.002, 0.002])
    sky_brightness = np.array([23.807, 25.517, 22.627, 22.307, 21.917, 22.257, 21.757, 21.567, 22.417, 22.537])
    fwhm_psf = 1.22 * central_wavelength * 0.000000001 * 206264.8062 / aperture
    fwhm_psf[fwhm_psf < diff_limit] = fwhm_psf[fwhm_psf < diff_limit] * 0.0 + diff_limit

    sn_box = np.round(3. * fwhm_psf / pixel_size) 

    number_of_exposures = np.array([3., 3., 3., 3., 3., 3., 3., 3., 3., 3.])

    desired_exposure_time = np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]) * exposure_in_hours * 3600.

    time_per_exposure = desired_exposure_time / number_of_exposures

    signal_counts = total_qe * desired_exposure_time * ab_zeropoint * aperture_correction * 0.7854 * \
        (aperture * 100.0)**2 * derived_bandpass * 10.**(-0.4*ab_magnitudes)

    shot_noise_in_signal = signal_counts ** 0.5

    sky_counts = total_qe * desired_exposure_time * ab_zeropoint * 0.7854 * (aperture * 100.0)**2 * \
        derived_bandpass * 10.**(-0.4*sky_brightness) * (pixel_size * sn_box)**2

    shot_noise_in_sky = sky_counts ** 0.5

    read_noise = detector_read_noise * sn_box * number_of_exposures**0.5

    dark_noise = sn_box * (dark_current * desired_exposure_time)**0.5

    snr = signal_counts / (signal_counts + sky_counts + read_noise**2 + dark_noise**2)**0.5


    print
    print
    print
    print 'source_mag', source_magnitudes
    print 'central wave', central_wavelength
    print 'ab zeropoints', ab_zeropoint
    print 'total_qe', total_qe
    print 'ap corr', aperture_correction
    print 'bandpass R', bandpass_r
    print 'derived_bandpass', derived_bandpass
    print 'read_noise', detector_read_noise
    print 'dark rate', dark_current
    print 'sky_brightness', sky_brightness
    print 'fwhm_psf', fwhm_psf
    print 'sn_box', sn_box
    print 'number_of_exposures', number_of_exposures
    print 'detector_read_noise', detector_read_noise
    print 'time_per_exp', time_per_exposure
    print 'signal_counts', signal_counts
    print 'shot_noise_in_signal', shot_noise_in_signal 
    print 'sky_counts', sky_counts
    print 'shot_noise_in_sky', shot_noise_in_sky 
    print 'read noise', read_noise
    print 'dark noise', dark_noise
    print 'SNR', snr, np.max(snr) 
    print
    print
    print

    return snr 
