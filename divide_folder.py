import os
import shutil

def divide_folder(folder_path, files_per_folder, dry_run):
	if not os.path.exists(folder_path):
		return

	els = os.listdir(folder_path)
	els = sorted(els)
	num_files = len(els)
	print('There are {} files to split'.format(num_files))
	chunk_size = files_per_folder

	chunked_files = [els[i:i + chunk_size] for i in range(0, num_files, chunk_size)]

	num_files_moved = 0
	i = 0
	for chunk in chunked_files:

		subfolder = os.path.join(folder_path, 'chunk{}'.format(i))
		if not os.path.exists(subfolder):
			print('mkdir {}'.format(subfolder))
			if not dry_run:
				os.mkdir(subfolder)

		for filename in chunk:
			prev_path = os.path.join(folder_path, filename)
			new_path = os.path.join(subfolder, filename)
			print('mv {} to {}'.format(prev_path, new_path))
			num_files_moved += 1
			if not dry_run:
				shutil.move(prev_path, new_path)
		
		print('')

		i += 1

	assert num_files_moved == num_files, f'{num_files_moved} != {num_files}'

def main():
	#folder_path = '/Users/dlluncor/Downloads/david_large_videos_250'
	#folder_path = '/Users/dlluncor/Downloads/deb_largest_50_videos'
	folder_path = '/Users/dlluncor/Downloads/deb_next_largest_100_videos'

	divide_folder(
		folder_path=folder_path,
		files_per_folder=15,
		dry_run=True
	)

	divide_folder(
		folder_path=folder_path,
		files_per_folder=15,
		dry_run=False
	)

if __name__ == '__main__':
	main()
